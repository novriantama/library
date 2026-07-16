from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import Book
from app.domain.repositories import BookRepository
from app.infrastructure.orm import BookORM

class SQLAlchemyBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, book_id: int) -> Optional[Book]:
        orm_book = self.db.query(BookORM).filter(BookORM.book_id == book_id).first()
        if not orm_book:
            return None
        return self._to_domain(orm_book)

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        orm_book = self.db.query(BookORM).filter(BookORM.isbn == isbn).first()
        if not orm_book:
            return None
        return self._to_domain(orm_book)

    def get_all(self) -> List[Book]:
        orm_books = self.db.query(BookORM).all()
        return [self._to_domain(orm) for orm in orm_books]

    def create(self, book: Book) -> Book:
        orm_book = BookORM(
            isbn=book.isbn,
            title=book.title,
            genre=book.genre,
            publish_date=book.publish_date
        )
        if book.book_id is not None:
            orm_book.book_id = book.book_id

        self.db.add(orm_book)
        self.db.commit()
        self.db.refresh(orm_book)
        return self._to_domain(orm_book)

    def update(self, book: Book) -> Book:
        orm_book = self.db.query(BookORM).filter(BookORM.book_id == book.book_id).first()
        if not orm_book:
            raise ValueError(f"Book with id {book.book_id} not found")

        orm_book.isbn = book.isbn
        orm_book.title = book.title
        orm_book.genre = book.genre
        orm_book.publish_date = book.publish_date
        self.db.commit()
        self.db.refresh(orm_book)
        return self._to_domain(orm_book)

    def delete(self, book_id: int) -> bool:
        orm_book = self.db.query(BookORM).filter(BookORM.book_id == book_id).first()
        if not orm_book:
            return False
        self.db.delete(orm_book)
        self.db.commit()
        return True

    def _to_domain(self, orm: BookORM) -> Book:
        return Book(
            book_id=orm.book_id,
            isbn=orm.isbn,
            title=orm.title,
            genre=orm.genre,
            publish_date=orm.publish_date
        )
