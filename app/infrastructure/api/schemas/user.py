from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Username (3-50 characters, alphanumeric and underscores only)"
    )
    email: str = Field(
        ...,
        max_length=255,
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        description="Valid email address"
    )

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, description="Plaintext password")
    user_id: Optional[int] = Field(None, description="Optional custom user ID")

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=6, max_length=100, description="Optional new plaintext password")

class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
