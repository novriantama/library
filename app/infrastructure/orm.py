from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

class AuthorORM(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    # Relationship to join table
    books = relationship(
        "BookAuthorORM",
        back_populates="author",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class BookORM(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    isbn = Column(String(13), unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    genre = Column(String(255), nullable=False)
    publish_date = Column(Date, nullable=True)

    # Relationship to join table
    authors = relationship(
        "BookAuthorORM",
        back_populates="book",
        cascade="all, delete-orphan",
        passive_deletes=True
    )


class BookAuthorORM(Base):
    __tablename__ = "book_authors"

    book_id = Column(Integer, ForeignKey("books.book_id", ondelete="CASCADE"), primary_key=True)
    author_id = Column(Integer, ForeignKey("authors.author_id", ondelete="CASCADE"), primary_key=True)
    role = Column(String(50), nullable=True)

    # Relationships to parents
    book = relationship("BookORM", back_populates="authors")
    author = relationship("AuthorORM", back_populates="books")


class UserORM(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

