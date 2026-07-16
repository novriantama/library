from datetime import date
from typing import List, Optional
from app.domain.entities import Book
from app.domain.repositories import BookRepository
from app.domain.exceptions import EntityNotFoundError, EntityAlreadyExistsError

class CreateBookUseCase:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def execute(self, isbn: str, title: str, genre: str, publish_date: Optional[date] = None, book_id: Optional[int] = None) -> Book:
        existing = self.book_repo.get_by_isbn(isbn)
        if existing:
            raise EntityAlreadyExistsError(f"Book with ISBN '{isbn}' already exists")

        book = Book(
            isbn=isbn,
            title=title,
            genre=genre,
            publish_date=publish_date,
            book_id=book_id
        )
        return self.book_repo.create(book)


class GetBookUseCase:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def get_by_id(self, book_id: int) -> Optional[Book]:
        return self.book_repo.get_by_id(book_id)

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.book_repo.get_by_isbn(isbn)

    def get_all(self) -> List[Book]:
        return self.book_repo.get_all()


class UpdateBookUseCase:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def execute(self, book_id: int, isbn: str, title: str, genre: str, publish_date: Optional[date] = None) -> Book:
        existing = self.book_repo.get_by_id(book_id)
        if not existing:
            raise EntityNotFoundError(f"Book with id {book_id} does not exist")

        if existing.isbn != isbn:
            conflict = self.book_repo.get_by_isbn(isbn)
            if conflict:
                raise EntityAlreadyExistsError(f"Book with ISBN '{isbn}' already exists")

        updated_book = Book(
            book_id=book_id,
            isbn=isbn,
            title=title,
            genre=genre,
            publish_date=publish_date
        )
        return self.book_repo.update(updated_book)


class DeleteBookUseCase:
    def __init__(self, book_repo: BookRepository):
        self.book_repo = book_repo

    def execute(self, book_id: int) -> bool:
        existing = self.book_repo.get_by_id(book_id)
        if not existing:
            raise EntityNotFoundError(f"Book with id {book_id} does not exist")
        return self.book_repo.delete(book_id)
