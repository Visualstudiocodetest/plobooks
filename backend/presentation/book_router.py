from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from services.book_service import BookService
from domain.book import Book
from presentation.schemas import BookCreate, BookRead, BookUpdate
from presentation.deps import get_db, require_admin

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookRead])
def list_books(db: Session = Depends(get_db)):
    service = BookService(db)
    return service.list_books()


@router.get("", response_model=List[BookRead], include_in_schema=False)
def list_books_no_slash(db: Session = Depends(get_db)):
    service = BookService(db)
    return service.list_books()


@router.get("/by-isbn/{isbn}", response_model=BookRead)
def get_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
    service = BookService(db)
    book = service.get_book_by_isbn(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/{id_article}", response_model=BookRead)
def get_book(id_article: int, db: Session = Depends(get_db)):
    service = BookService(db)
    book = service.get_book(id_article)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    service = BookService(db)
    book = Book(
        id_article=0,  # Will be set by DB
        id_type_objet=book_in.id_type_objet,
        id_etat_usure=book_in.id_etat_usure,
        titre=book_in.titre,
        isbn=book_in.isbn,
        auteur=book_in.auteur,
        editeur=book_in.editeur,
        date_publication=book_in.date_publication,
        langue=book_in.langue,
        description=book_in.description,
        image_link=book_in.image_link,
        prix_chf=book_in.prix_chf,
        actif=book_in.actif,
    )
    # require authentication to create
    return service.create_book(book)


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def create_book_no_slash(book_in: BookCreate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    service = BookService(db)
    book = Book(
        id_article=0,  # Will be set by DB
        id_type_objet=book_in.id_type_objet,
        id_etat_usure=book_in.id_etat_usure,
        titre=book_in.titre,
        isbn=book_in.isbn,
        auteur=book_in.auteur,
        editeur=book_in.editeur,
        date_publication=book_in.date_publication,
        langue=book_in.langue,
        description=book_in.description,
        image_link=book_in.image_link,
        prix_chf=book_in.prix_chf,
        actif=book_in.actif,
    )
    return service.create_book(book)

@router.put("/{id_article}", response_model=BookRead)
def update_book(id_article: int, book_update: BookUpdate, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    service = BookService(db)
    updated = service.update_book(id_article, book_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@router.delete("/{id_article}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id_article: int, db: Session = Depends(get_db), _admin=Depends(require_admin)):
    service = BookService(db)
    deleted = service.delete_book(id_article)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
