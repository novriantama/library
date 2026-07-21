# pyrefly: ignore [missing-import]
from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db

# Repositories
from app.infrastructure.repositories.author_repository import SQLAlchemyAuthorRepository
from app.infrastructure.repositories.book_repository import SQLAlchemyBookRepository
from app.infrastructure.repositories.book_author_repository import SQLAlchemyBookAuthorRepository
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository


# Use Cases
from app.use_cases.author import (
    CreateAuthorUseCase,
    GetAuthorUseCase,
    UpdateAuthorUseCase,
    DeleteAuthorUseCase,
)
from app.use_cases.book import (
    CreateBookUseCase,
    GetBookUseCase,
    UpdateBookUseCase,
    DeleteBookUseCase,
)
from app.use_cases.book_author import (
    AssignAuthorToBookUseCase,
    UpdateBookAuthorRoleUseCase,
    RemoveAuthorFromBookUseCase,
    GetBookAuthorsUseCase,
)
from app.use_cases.user import (
    CreateUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)

# --- AUTHOR DEPENDENCIES ---

def get_author_repository(db: Session = Depends(get_db)) -> SQLAlchemyAuthorRepository:
    return SQLAlchemyAuthorRepository(db)

def get_create_author_use_case(
    repo: SQLAlchemyAuthorRepository = Depends(get_author_repository)
) -> CreateAuthorUseCase:
    return CreateAuthorUseCase(repo)

def get_get_author_use_case(
    repo: SQLAlchemyAuthorRepository = Depends(get_author_repository)
) -> GetAuthorUseCase:
    return GetAuthorUseCase(repo)

def get_update_author_use_case(
    repo: SQLAlchemyAuthorRepository = Depends(get_author_repository)
) -> UpdateAuthorUseCase:
    return UpdateAuthorUseCase(repo)

def get_delete_author_use_case(
    repo: SQLAlchemyAuthorRepository = Depends(get_author_repository)
) -> DeleteAuthorUseCase:
    return DeleteAuthorUseCase(repo)


# --- BOOK DEPENDENCIES ---

def get_book_repository(db: Session = Depends(get_db)) -> SQLAlchemyBookRepository:
    return SQLAlchemyBookRepository(db)

def get_create_book_use_case(
    repo: SQLAlchemyBookRepository = Depends(get_book_repository)
) -> CreateBookUseCase:
    return CreateBookUseCase(repo)

def get_get_book_use_case(
    repo: SQLAlchemyBookRepository = Depends(get_book_repository)
) -> GetBookUseCase:
    return GetBookUseCase(repo)

def get_update_book_use_case(
    repo: SQLAlchemyBookRepository = Depends(get_book_repository)
) -> UpdateBookUseCase:
    return UpdateBookUseCase(repo)

def get_delete_book_use_case(
    repo: SQLAlchemyBookRepository = Depends(get_book_repository)
) -> DeleteBookUseCase:
    return DeleteBookUseCase(repo)


# --- BOOK-AUTHOR DEPENDENCIES ---

def get_book_author_repository(db: Session = Depends(get_db)) -> SQLAlchemyBookAuthorRepository:
    return SQLAlchemyBookAuthorRepository(db)

def get_assign_author_to_book_use_case(
    book_author_repo: SQLAlchemyBookAuthorRepository = Depends(get_book_author_repository),
    book_repo: SQLAlchemyBookRepository = Depends(get_book_repository),
    author_repo: SQLAlchemyAuthorRepository = Depends(get_author_repository),
) -> AssignAuthorToBookUseCase:
    return AssignAuthorToBookUseCase(book_author_repo, book_repo, author_repo)

def get_update_book_author_role_use_case(
    repo: SQLAlchemyBookAuthorRepository = Depends(get_book_author_repository)
) -> UpdateBookAuthorRoleUseCase:
    return UpdateBookAuthorRoleUseCase(repo)

def get_remove_author_from_book_use_case(
    repo: SQLAlchemyBookAuthorRepository = Depends(get_book_author_repository)
) -> RemoveAuthorFromBookUseCase:
    return RemoveAuthorFromBookUseCase(repo)

def get_get_book_authors_use_case(
    repo: SQLAlchemyBookAuthorRepository = Depends(get_book_author_repository)
) -> GetBookAuthorsUseCase:
    return GetBookAuthorsUseCase(repo)


# --- USER DEPENDENCIES ---

def get_user_repository(db: Session = Depends(get_db)) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(db)

def get_create_user_use_case(
    repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)

def get_get_user_use_case(
    repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> GetUserUseCase:
    return GetUserUseCase(repo)

def get_update_user_use_case(
    repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> UpdateUserUseCase:
    return UpdateUserUseCase(repo)

def get_delete_user_use_case(
    repo: SQLAlchemyUserRepository = Depends(get_user_repository)
) -> DeleteUserUseCase:
    return DeleteUserUseCase(repo)

