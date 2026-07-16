from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class BookAuthorBase(BaseModel):
    role: Optional[str] = Field(None, max_length=50, description="Role of the author (e.g. Lead Author, Co-Author, Illustrator)")

class BookAuthorCreate(BookAuthorBase):
    book_id: int = Field(..., description="ID of the book")
    author_id: int = Field(..., description="ID of the author")

class BookAuthorUpdate(BookAuthorBase):
    pass

class BookAuthorResponse(BookAuthorBase):
    book_id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)
