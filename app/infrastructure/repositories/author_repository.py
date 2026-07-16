from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities import Author
from app.domain.repositories import AuthorRepository
from app.infrastructure.orm import AuthorORM

class SQLAlchemyAuthorRepository(AuthorRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, author_id: int) -> Optional[Author]:
        orm_author = self.db.query(AuthorORM).filter(AuthorORM.author_id == author_id).first()
        if not orm_author:
            return None
        return self._to_domain(orm_author)

    def get_all(self) -> List[Author]:
        orm_authors = self.db.query(AuthorORM).all()
        return [self._to_domain(orm) for orm in orm_authors]

    def create(self, author: Author) -> Author:
        orm_author = AuthorORM(
            first_name=author.first_name,
            last_name=author.last_name
        )
        # If client explicitly provides an author_id, we use it
        if author.author_id is not None:
            orm_author.author_id = author.author_id

        self.db.add(orm_author)
        self.db.commit()
        self.db.refresh(orm_author)
        return self._to_domain(orm_author)

    def update(self, author: Author) -> Author:
        orm_author = self.db.query(AuthorORM).filter(AuthorORM.author_id == author.author_id).first()
        if not orm_author:
            raise ValueError(f"Author with id {author.author_id} not found")

        orm_author.first_name = author.first_name
        orm_author.last_name = author.last_name
        self.db.commit()
        self.db.refresh(orm_author)
        return self._to_domain(orm_author)

    def delete(self, author_id: int) -> bool:
        orm_author = self.db.query(AuthorORM).filter(AuthorORM.author_id == author_id).first()
        if not orm_author:
            return False
        self.db.delete(orm_author)
        self.db.commit()
        return True

    def _to_domain(self, orm: AuthorORM) -> Author:
        return Author(
            author_id=orm.author_id,
            first_name=orm.first_name,
            last_name=orm.last_name
        )
