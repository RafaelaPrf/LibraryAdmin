import csv
import random
from sqlalchemy import (
    create_engine, Column, Integer, String, ForeignKey, Table, Float,
    CheckConstraint
)
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


book_tags = Table(
    'book_tags', Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)


class Genre(Base):

    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    books = relationship("Book", back_populates="genre")


class Author(Base):

    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50), nullable=True)

    books = relationship("Book", back_populates="author")


class Tag(Base):

    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    books = relationship("Book", secondary=book_tags, back_populates="tags")


class Book(Base):

    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    upc = Column(String(20), nullable=False, unique=True)

    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    genre = relationship("Genre", back_populates="books")
    author = relationship("Author", back_populates="books")
    tags = relationship("Tag", secondary=book_tags, back_populates="books")

    detail = relationship("BookDetail", back_populates="book", uselist=False) # book.details instead of book.detail[0]


class BookDetail(Base):

    __tablename__ = 'book_details'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False, unique=True)

    rating = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    availability = Column(Integer, nullable=False)

    book = relationship("Book", back_populates="detail")

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
        CheckConstraint('price >= 0', name='check_positive_price'),
        CheckConstraint('availability >= 0', name='check_nonnegative_availability'),
    )


SYNTHETIC_AUTHORS = [
    ("Alice Munro", "Canada"),
    ("Haruki Murakami", "Japan"),
    ("Chimamanda Ngozi Adichie", "Nigeria"),
    ("Margaret Atwood", "Canada"),
    ("Kazuo Ishiguro", "United Kingdom"),
    ("Elena Ferrante", "Italy"),
    ("Neil Gaiman", "United Kingdom"),
    ("Toni Morrison", "United States"),
    ("Yann Martel", "Canada"),
    ("Isabel Allende", "Chile"),
]

SYNTHETIC_TAGS = [
    "bestseller", "award-winning", "staff-pick", "translated",
    "illustrated", "series", "debut", "classic", "signed-copy", "limited-edition"
]


def load_books_from_csv(path):
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


if __name__ == "__main__":
    engine = create_engine('postgresql://postgres:admin@localhost/postgres')

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    csv_rows = load_books_from_csv('books.csv')

    distinct_genre_names = sorted({row['genre'] for row in csv_rows})
    genre_objs = {name: Genre(name=name) for name in distinct_genre_names}
    session.add_all(genre_objs.values())
    session.commit()

    author_objs = [Author(name=name, country=country) for name, country in SYNTHETIC_AUTHORS]
    session.add_all(author_objs)
    session.commit()

    tag_objs = [Tag(name=name) for name in SYNTHETIC_TAGS]
    session.add_all(tag_objs)
    session.commit()

    books = []
    for i, row in enumerate(csv_rows):
        genre = genre_objs[row['genre']]
        author = random.choice(author_objs)

        book = Book(
            title=row['title'],
            upc=row['upc'],
            genre=genre,
            author=author,
        )

        book.tags = random.sample(tag_objs, random.randint(0, 3))

        books.append(book)

    session.add_all(books)
    session.commit()

    details = []
    for row, book in zip(csv_rows, books):
        detail = BookDetail(
            book=book,
            rating=RATING_MAP[row['rating']],
            price=float(row['price']),
            availability=int(row['availability']),
        )
        details.append(detail)

    session.add_all(details)
    session.commit()

    print(f"Loaded {len(books)} books across {len(genre_objs)} genres, "
          f"{len(author_objs)} authors, and {len(tag_objs)} tags.")