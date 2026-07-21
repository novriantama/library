import bcrypt
from typing import List, Optional
from app.domain.entities import User
from app.domain.repositories import UserRepository
from app.domain.exceptions import EntityNotFoundError, EntityAlreadyExistsError

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')


class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str, email: str, password: str, user_id: Optional[int] = None) -> User:
        # Business logic validation: unique username
        if self.user_repo.get_by_username(username):
            raise EntityAlreadyExistsError(f"User with username '{username}' already exists")

        # Business logic validation: unique email
        if self.user_repo.get_by_email(email):
            raise EntityAlreadyExistsError(f"User with email '{email}' already exists")

        # Hash the password
        password_hash = hash_password(password)

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            user_id=user_id
        )
        return self.user_repo.create(user)


class GetUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.user_repo.get_by_id(user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.user_repo.get_by_username(username)

    def get_all(self) -> List[User]:
        return self.user_repo.get_all()


class UpdateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int, username: str, email: str, password: Optional[str] = None) -> User:
        existing = self.user_repo.get_by_id(user_id)
        if not existing:
            raise EntityNotFoundError(f"User with id {user_id} does not exist")

        # Validation: unique username if changed
        if existing.username != username:
            conflict = self.user_repo.get_by_username(username)
            if conflict:
                raise EntityAlreadyExistsError(f"User with username '{username}' already exists")

        # Validation: unique email if changed
        if existing.email != email:
            conflict = self.user_repo.get_by_email(email)
            if conflict:
                raise EntityAlreadyExistsError(f"User with email '{email}' already exists")

        # Password encryption (only hash if new password is provided)
        if password:
            password_hash = hash_password(password)
        else:
            password_hash = existing.password_hash

        updated_user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            created_at=existing.created_at
        )
        return self.user_repo.update(updated_user)


class DeleteUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, user_id: int) -> bool:
        existing = self.user_repo.get_by_id(user_id)
        if not existing:
            raise EntityNotFoundError(f"User with id {user_id} does not exist")
        return self.user_repo.delete(user_id)
