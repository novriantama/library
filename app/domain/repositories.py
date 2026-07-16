from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Author, Book, BookAuthor

class AuthorRepository(ABC):
    @abstractmethod
    def get_by_id(self, author_id: int) -> Optional[Author]:
        """Retrieve an Author by their ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[Author]:
        """Retrieve all Authors."""
        pass

    @abstractmethod
    def create(self, author: Author) -> Author:
        """Create a new Author."""
        pass

    @abstractmethod
    def update(self, author: Author) -> Author:
        """Update an existing Author's details."""
        pass

    @abstractmethod
    def delete(self, author_id: int) -> bool:
        """Delete an Author by their ID."""
        pass

class BookRepository(ABC):
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        """Retrieve a Book by its ID."""
        pass

    @abstractmethod
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        """Retrieve a Book by its unique ISBN."""
        pass

    @abstractmethod
    def get_all(self) -> List[Book]:
        """Retrieve all Books."""
        pass

    @abstractmethod
    def create(self, book: Book) -> Book:
        """Create a new Book."""
        pass

    @abstractmethod
    def update(self, book: Book) -> Book:
        """Update an existing Book's details."""
        pass

    @abstractmethod
    def delete(self, book_id: int) -> bool:
        """Delete a Book by its ID."""
        pass

class BookAuthorRepository(ABC):
    @abstractmethod
    def get_by_ids(self, book_id: int, author_id: int) -> Optional[BookAuthor]:
        """Retrieve a specific BookAuthor relationship."""
        pass

    @abstractmethod
    def get_by_book_id(self, book_id: int) -> List[BookAuthor]:
        """Retrieve all BookAuthor relationships for a specific Book."""
        pass

    @abstractmethod
    def get_by_author_id(self, author_id: int) -> List[BookAuthor]:
        """Retrieve all BookAuthor relationships for a specific Author."""
        pass

    @abstractmethod
    def get_all(self) -> List[BookAuthor]:
        """Retrieve all BookAuthor relationships."""
        pass

    @abstractmethod
    def create(self, book_author: BookAuthor) -> BookAuthor:
        """Create a new BookAuthor relationship."""
        pass

    @abstractmethod
    def update(self, book_author: BookAuthor) -> BookAuthor:
        """Update a BookAuthor relationship (e.g. role)."""
        pass

    @abstractmethod
    def delete(self, book_id: int, author_id: int) -> bool:
        """Delete a BookAuthor relationship by composite keys."""
        pass
