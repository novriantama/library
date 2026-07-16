from typing import List, Optional
from app.domain.entities import Author
from app.domain.repositories import AuthorRepository
from app.domain.exceptions import EntityNotFoundError

class CreateAuthorUseCase:
    def __init__(self, author_repo: AuthorRepository):
        self.author_repo = author_repo

    def execute(self, first_name: str, last_name: str, author_id: Optional[int] = None) -> Author:
        author = Author(
            first_name=first_name,
            last_name=last_name,
            author_id=author_id
        )
        return self.author_repo.create(author)


class GetAuthorUseCase:
    def __init__(self, author_repo: AuthorRepository):
        self.author_repo = author_repo

    def get_by_id(self, author_id: int) -> Optional[Author]:
        return self.author_repo.get_by_id(author_id)

    def get_all(self) -> List[Author]:
        return self.author_repo.get_all()


class UpdateAuthorUseCase:
    def __init__(self, author_repo: AuthorRepository):
        self.author_repo = author_repo

    def execute(self, author_id: int, first_name: str, last_name: str) -> Author:
        existing = self.author_repo.get_by_id(author_id)
        if not existing:
            raise EntityNotFoundError(f"Author with id {author_id} does not exist")

        updated_author = Author(
            author_id=author_id,
            first_name=first_name,
            last_name=last_name
        )
        return self.author_repo.update(updated_author)


class DeleteAuthorUseCase:
    def __init__(self, author_repo: AuthorRepository):
        self.author_repo = author_repo

    def execute(self, author_id: int) -> bool:
        existing = self.author_repo.get_by_id(author_id)
        if not existing:
            raise EntityNotFoundError(f"Author with id {author_id} does not exist")
        return self.author_repo.delete(author_id)
