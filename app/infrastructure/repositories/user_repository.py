from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import User
from app.domain.repositories import UserRepository
from app.infrastructure.orm import UserORM

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        orm_user = self.db.query(UserORM).filter(UserORM.user_id == user_id).first()
        if not orm_user:
            return None
        return self._to_domain(orm_user)

    def get_by_username(self, username: str) -> Optional[User]:
        orm_user = self.db.query(UserORM).filter(UserORM.username == username).first()
        if not orm_user:
            return None
        return self._to_domain(orm_user)

    def get_by_email(self, email: str) -> Optional[User]:
        orm_user = self.db.query(UserORM).filter(UserORM.email == email).first()
        if not orm_user:
            return None
        return self._to_domain(orm_user)

    def get_all(self) -> List[User]:
        orm_users = self.db.query(UserORM).all()
        return [self._to_domain(orm) for orm in orm_users]

    def create(self, user: User) -> User:
        orm_user = UserORM(
            username=user.username,
            email=user.email,
            password_hash=user.password_hash
        )
        if user.user_id is not None:
            orm_user.user_id = user.user_id

        self.db.add(orm_user)
        self.db.commit()
        self.db.refresh(orm_user)
        return self._to_domain(orm_user)

    def update(self, user: User) -> User:
        orm_user = self.db.query(UserORM).filter(UserORM.user_id == user.user_id).first()
        if not orm_user:
            raise ValueError(f"User with id {user.user_id} not found")

        orm_user.username = user.username
        orm_user.email = user.email
        orm_user.password_hash = user.password_hash
        self.db.commit()
        self.db.refresh(orm_user)
        return self._to_domain(orm_user)

    def delete(self, user_id: int) -> bool:
        orm_user = self.db.query(UserORM).filter(UserORM.user_id == user_id).first()
        if not orm_user:
            return False
        self.db.delete(orm_user)
        self.db.commit()
        return True

    def _to_domain(self, orm: UserORM) -> User:
        return User(
            user_id=orm.user_id,
            username=orm.username,
            email=orm.email,
            password_hash=orm.password_hash,
            created_at=orm.created_at
        )
