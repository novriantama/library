from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    username: str = Field(..., description="Username of the user")
    password: str = Field(..., description="Plaintext password of the user")

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Encoded JWT access token")
    token_type: str = Field("bearer", description="Token type")

class LogoutResponse(BaseModel):
    message: str = Field("Successfully logged out", description="Logout status message")
