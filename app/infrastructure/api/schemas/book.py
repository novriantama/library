from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class BookBase(BaseModel):
    isbn: str = Field(
        ...,
        min_length=13,
        max_length=13,
        pattern=r"^\d{13}$",
        description="International Standard Book Number (exactly 13 digits)"
    )
    title: str = Field(..., min_length=1, max_length=255, description="Title of the book")
    genre: str = Field(..., min_length=1, max_length=255, description="Genre of the book")
    publish_date: Optional[date] = Field(None, description="Publish date in YYYY-MM-DD format")

class BookCreate(BookBase):
    book_id: Optional[int] = Field(None, description="Optional custom ID for the book")

class BookUpdate(BookBase):
    pass

class BookResponse(BookBase):
    book_id: int

    model_config = ConfigDict(from_attributes=True)
