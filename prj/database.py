from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from create_tables import Book, BookDetail, Genre, Author, Tag

DATABASE_URL = "postgresql://postgres:admin@localhost/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic schemas

class GenreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class AuthorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    country: Optional[str] = None


class TagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    upc: str
    genre_id: int
    author_id: int


class BookCreate(BaseModel):
    title: str
    upc: str
    genre_id: int
    author_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    upc: Optional[str] = None
    genre_id: Optional[int] = None
    author_id: Optional[int] = None


class BookDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    book_id: int
    rating: int
    price: float
    availability: int


class BookDetailCreate(BaseModel):
    book_id: int
    rating: int
    price: float
    availability: int



# Books

@app.get("/books", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db)):

    return db.query(Book).all()


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):

    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):

    if not db.query(Genre).filter(Genre.id == payload.genre_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="genre_id does not exist")
    if not db.query(Author).filter(Author.id == payload.author_id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="author_id does not exist")
    if db.query(Book).filter(Book.upc == payload.upc).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="upc already exists")

    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):

    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    print(payload)
    update_data = payload.model_dump(exclude_unset=True)

    if "genre_id" in update_data and not db.query(Genre).filter(Genre.id == update_data["genre_id"]).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="genre_id does not exist")
    if "author_id" in update_data and not db.query(Author).filter(Author.id == update_data["author_id"]).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="author_id does not exist")

    for field, value in update_data.items():
        setattr(book, field, value)
    print(update_data)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    if book.detail is not None:
        db.delete(book.detail)
    book.tags = []  # clears the book_tags association rows for this book
    db.delete(book)
    db.commit()
    return None



# Book details:
@app.get("/book-details", response_model=List[BookDetailOut])
def get_book_details(db: Session = Depends(get_db)):

    return db.query(BookDetail).all()


@app.get("/book-details/{detail_id}", response_model=BookDetailOut)
def get_book_detail(detail_id: int, db: Session = Depends(get_db)):

    detail = db.query(BookDetail).filter(BookDetail.id == detail_id).first()
    if detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book detail not found")
    return detail


@app.post("/book-details", response_model=BookDetailOut, status_code=status.HTTP_201_CREATED)
def create_book_detail(payload: BookDetailCreate, db: Session = Depends(get_db)):
    # book_id is unique, enforcing the one-to-one relationship
    book = db.query(Book).filter(Book.id == payload.book_id).first()
    if book is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="book_id does not exist")
    if book.detail is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This book already has a book_details row")
    if not (1 <= payload.rating <= 5):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="rating must be between 1 and 5")
    if payload.price < 0 or payload.availability < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="price and availability must be non-negative")

    detail = BookDetail(**payload.model_dump())
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail


@app.delete("/book-details/{detail_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_detail(detail_id: int, db: Session = Depends(get_db)):

    detail = db.query(BookDetail).filter(BookDetail.id == detail_id).first()
    if detail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book detail not found")
    db.delete(detail)
    db.commit()
    return None


@app.get("/genres", response_model=List[GenreOut])
def get_genres(db: Session = Depends(get_db)):

    return db.query(Genre).all()


@app.get("/authors", response_model=List[AuthorOut])
def get_authors(db: Session = Depends(get_db)):

    return db.query(Author).all()


@app.get("/tags", response_model=List[TagOut])
def get_tags(db: Session = Depends(get_db)):

    return db.query(Tag).all()


@app.get("/books/by_author/{name}", response_model=List[BookOut])
def get_books_by_author(name: str, db: Session = Depends(get_db)):
    author = db.query(Author).filter(Author.name == name).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author.books


@app.get("/books/by-rating/{min_rating}", response_model=List[BookOut])
def get_books_by_rating(min_rating: int, db: Session = Depends(get_db)):
    if not (1 <= min_rating <= 5):
        raise HTTPException(status_code=400, detail="min_rating must be between 1 and 5")
    books = db.query(Book).join(BookDetail).filter(BookDetail.rating >= min_rating).all()
    return books