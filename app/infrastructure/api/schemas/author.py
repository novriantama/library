from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class AuthorBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, description="Author's first name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Author's last name")

class AuthorCreate(AuthorBase):
    author_id: Optional[int] = Field(None, description="Optional custom ID for the author")

class AuthorUpdate(AuthorBase):
    pass

class AuthorResponse(AuthorBase):
    author_id: int

    model_config = ConfigDict(from_attributes=True)
