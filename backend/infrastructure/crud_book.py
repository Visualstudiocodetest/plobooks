"""
CRUD operations for Book/Livre and Article tables using SQLAlchemy.

- get_books: List all books
- get_book: Retrieve a book by id
- create_book: Insert a new book
- update_book: Update a book
- delete_book: Delete a book

All functions expect a SQLAlchemy Session as first argument.
"""
from sqlalchemy.orm import Session
from infrastructure import models
from domain.book import Book
from typing import List, Optional

def _ensure_default_refs(db: Session, book: Book) -> tuple[int, int]:
    """
    Ensure Article foreign keys exist.
    We keep this very small and deterministic for local/dev DBs:
    - TypeObjet: try requested id, else code='BOOK', else first row, else create default.
    - EtatUsure: try requested id, else libelle='Neuf', else first row, else create default.
    """
    type_objet = None
    if getattr(book, "id_type_objet", 0):
        type_objet = (
            db.query(models.TypeObjet).filter(models.TypeObjet.id_type_objet == int(book.id_type_objet)).first()
        )
    if type_objet is None:
        type_objet = db.query(models.TypeObjet).filter(models.TypeObjet.code == "BOOK").first()
    if type_objet is None:
        type_objet = db.query(models.TypeObjet).order_by(models.TypeObjet.id_type_objet.asc()).first()
    if type_objet is None:
        type_objet = models.TypeObjet(libelle="Livre", code="BOOK", description="Type par défaut (tests/dev)")
        db.add(type_objet)
        db.flush()

    etat = None
    if getattr(book, "id_etat_usure", 0):
        etat = (
            db.query(models.EtatUsure).filter(models.EtatUsure.id_etat_usure == int(book.id_etat_usure)).first()
        )
    if etat is None:
        etat = db.query(models.EtatUsure).filter(models.EtatUsure.libelle == "Neuf").first()
    if etat is None:
        etat = db.query(models.EtatUsure).order_by(models.EtatUsure.id_etat_usure.asc()).first()
    if etat is None:
        etat = models.EtatUsure(libelle="Neuf", description="État par défaut (tests/dev)")
        db.add(etat)
        db.flush()

    return int(type_objet.id_type_objet), int(etat.id_etat_usure)

def get_books(db: Session) -> List[models.Livre]:
    """Return all books (Livre + Article)."""
    return db.query(models.Livre).all()

def get_book(db: Session, id_article: int) -> Optional[models.Livre]:
    """Return a book by article ID."""
    return db.query(models.Livre).filter(models.Livre.id_article == id_article).first()


def get_book_by_isbn(db: Session, isbn: str) -> Optional[models.Livre]:
    """Return a book by ISBN (exact match)."""
    return db.query(models.Livre).filter(models.Livre.isbn == isbn).first()

def create_book(db: Session, book: Book) -> models.Livre:
    """Insert a new book and its article."""
    id_type_objet, id_etat_usure = _ensure_default_refs(db, book)
    db_article = models.Article(
        id_type_objet=id_type_objet,
        id_etat_usure=id_etat_usure,
        sku=book.isbn,
        titre=book.titre,
        description=book.description,
        image_link=book.image_link,
        prix_chf=book.prix_chf,
        actif=book.actif,
    )
    db.add(db_article)
    db.flush()  # Get id_article
    db_livre = models.Livre(
        id_article=db_article.id_article,
        isbn=book.isbn,
        auteur=book.auteur,
        editeur=book.editeur,
        date_publication=book.date_publication,
        langue=book.langue,
    )
    db.add(db_livre)
    db.commit()
    db.refresh(db_livre)
    return db_livre

def update_book(db: Session, id_article: int, data: dict) -> Optional[models.Livre]:
    """Update a book and/or its article."""
    db_livre = db.query(models.Livre).filter(models.Livre.id_article == id_article).first()
    if not db_livre:
        return None
    db_article = db_livre.article
    for key, value in data.items():
        if hasattr(db_livre, key):
            setattr(db_livre, key, value)
        elif hasattr(db_article, key):
            setattr(db_article, key, value)
    db.commit()
    db.refresh(db_livre)
    return db_livre

def delete_book(db: Session, id_article: int) -> bool:
    """Delete a book and its article."""
    db_livre = db.query(models.Livre).filter(models.Livre.id_article == id_article).first()
    if not db_livre:
        return False
    db.delete(db_livre)
    db.commit()
    return True
