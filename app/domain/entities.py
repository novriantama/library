from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Author:
    first_name: str
    last_name: str
    author_id: Optional[int] = None

@dataclass
class Book:
    isbn: str
    title: str
    genre: str
    publish_date: Optional[date] = None
    book_id: Optional[int] = None

@dataclass
class BookAuthor:
    book_id: int
    author_id: int
    role: Optional[str] = None

@dataclass
class User:
    username: str
    email: str
    password_hash: str
    created_at: Optional[datetime] = None
    user_id: Optional[int] = None

