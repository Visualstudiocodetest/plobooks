from typing import List, Optional
from domain.book import Book
from infrastructure.db import SessionLocal
from infrastructure import crud_book

class BookService:
    def __init__(self, db_session=None):
        self.db_session = db_session or SessionLocal()

    def list_books(self) -> List[Book]:
        db_livres = crud_book.get_books(self.db_session)
        return [self._to_domain_book(livre) for livre in db_livres]

    def get_book(self, id_article: int) -> Optional[Book]:
        db_livre = crud_book.get_book(self.db_session, id_article)
        if db_livre:
            return self._to_domain_book(db_livre)
        return None

    def create_book(self, book: Book) -> Book:
        db_livre = crud_book.create_book(self.db_session, book)
        return self._to_domain_book(db_livre)

    def update_book(self, id_article: int, data: dict) -> Optional[Book]:
        db_livre = crud_book.update_book(self.db_session, id_article, data)
        if db_livre:
            return self._to_domain_book(db_livre)
        return None

    def delete_book(self, id_article: int) -> bool:
        return crud_book.delete_book(self.db_session, id_article)

    def _to_domain_book(self, db_livre):
        article = db_livre.article
        return Book(
            id_article=db_livre.id_article,
            titre=article.titre,
            isbn=db_livre.isbn,
            auteur=db_livre.auteur,
            editeur=db_livre.editeur,
            date_publication=db_livre.date_publication,
            langue=db_livre.langue,
            description=article.description,
            image_link=article.image_link,
            prix_chf=float(article.prix_chf),
            actif=article.actif,
        )
