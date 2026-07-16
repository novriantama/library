from typing import List, Optional
from app.domain.entities import BookAuthor
from app.domain.repositories import BookAuthorRepository, BookRepository, AuthorRepository
from app.domain.exceptions import EntityNotFoundError, EntityAlreadyExistsError

class AssignAuthorToBookUseCase:
    def __init__(
        self,
        book_author_repo: BookAuthorRepository,
        book_repo: BookRepository,
        author_repo: AuthorRepository
    ):
        self.book_author_repo = book_author_repo
        self.book_repo = book_repo
        self.author_repo = author_repo

    def execute(self, book_id: int, author_id: int, role: Optional[str] = None) -> BookAuthor:
        if not self.book_repo.get_by_id(book_id):
            raise EntityNotFoundError(f"Book with id {book_id} does not exist")

        if not self.author_repo.get_by_id(author_id):
            raise EntityNotFoundError(f"Author with id {author_id} does not exist")

        if self.book_author_repo.get_by_ids(book_id, author_id):
            raise EntityAlreadyExistsError(
                f"Author with id {author_id} is already assigned to book with id {book_id}"
            )

        book_author = BookAuthor(book_id=book_id, author_id=author_id, role=role)
        return self.book_author_repo.create(book_author)


class UpdateBookAuthorRoleUseCase:
    def __init__(self, book_author_repo: BookAuthorRepository):
        self.book_author_repo = book_author_repo

    def execute(self, book_id: int, author_id: int, role: Optional[str] = None) -> BookAuthor:
        existing = self.book_author_repo.get_by_ids(book_id, author_id)
        if not existing:
            raise EntityNotFoundError(
                f"No assignment found between book_id {book_id} and author_id {author_id}"
            )

        updated = BookAuthor(book_id=book_id, author_id=author_id, role=role)
        return self.book_author_repo.update(updated)


class RemoveAuthorFromBookUseCase:
    def __init__(self, book_author_repo: BookAuthorRepository):
        self.book_author_repo = book_author_repo

    def execute(self, book_id: int, author_id: int) -> bool:
        existing = self.book_author_repo.get_by_ids(book_id, author_id)
        if not existing:
            raise EntityNotFoundError(
                f"No assignment found between book_id {book_id} and author_id {author_id}"
            )
        return self.book_author_repo.delete(book_id, author_id)


class GetBookAuthorsUseCase:
    def __init__(self, book_author_repo: BookAuthorRepository):
        self.book_author_repo = book_author_repo

    def get_by_ids(self, book_id: int, author_id: int) -> Optional[BookAuthor]:
        return self.book_author_repo.get_by_ids(book_id, author_id)

    def get_by_book_id(self, book_id: int) -> List[BookAuthor]:
        return self.book_author_repo.get_by_book_id(book_id)

    def get_by_author_id(self, author_id: int) -> List[BookAuthor]:
        return self.book_author_repo.get_by_author_id(author_id)

    def get_all(self) -> List[BookAuthor]:
        return self.book_author_repo.get_all()
