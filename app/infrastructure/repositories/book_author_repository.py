from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import BookAuthor
from app.domain.repositories import BookAuthorRepository
from app.infrastructure.orm import BookAuthorORM

class SQLAlchemyBookAuthorRepository(BookAuthorRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_ids(self, book_id: int, author_id: int) -> Optional[BookAuthor]:
        orm = self.db.query(BookAuthorORM).filter(
            BookAuthorORM.book_id == book_id,
            BookAuthorORM.author_id == author_id
        ).first()
        if not orm:
            return None
        return self._to_domain(orm)

    def get_by_book_id(self, book_id: int) -> List[BookAuthor]:
        orm_list = self.db.query(BookAuthorORM).filter(BookAuthorORM.book_id == book_id).all()
        return [self._to_domain(orm) for orm in orm_list]

    def get_by_author_id(self, author_id: int) -> List[BookAuthor]:
        orm_list = self.db.query(BookAuthorORM).filter(BookAuthorORM.author_id == author_id).all()
        return [self._to_domain(orm) for orm in orm_list]

    def get_all(self) -> List[BookAuthor]:
        orm_list = self.db.query(BookAuthorORM).all()
        return [self._to_domain(orm) for orm in orm_list]

    def create(self, book_author: BookAuthor) -> BookAuthor:
        orm = BookAuthorORM(
            book_id=book_author.book_id,
            author_id=book_author.author_id,
            role=book_author.role
        )
        self.db.add(orm)
        self.db.commit()
        self.db.refresh(orm)
        return self._to_domain(orm)

    def update(self, book_author: BookAuthor) -> BookAuthor:
        orm = self.db.query(BookAuthorORM).filter(
            BookAuthorORM.book_id == book_author.book_id,
            BookAuthorORM.author_id == book_author.author_id
        ).first()
        if not orm:
            raise ValueError(
                f"Relationship between book_id {book_author.book_id} and "
                f"author_id {book_author.author_id} not found"
            )

        orm.role = book_author.role
        self.db.commit()
        self.db.refresh(orm)
        return self._to_domain(orm)

    def delete(self, book_id: int, author_id: int) -> bool:
        orm = self.db.query(BookAuthorORM).filter(
            BookAuthorORM.book_id == book_id,
            BookAuthorORM.author_id == author_id
        ).first()
        if not orm:
            return False
        self.db.delete(orm)
        self.db.commit()
        return True

    def _to_domain(self, orm: BookAuthorORM) -> BookAuthor:
        return BookAuthor(
            book_id=orm.book_id,
            author_id=orm.author_id,
            role=orm.role
        )
