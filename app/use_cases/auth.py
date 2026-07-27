import bcrypt
from typing import Dict, Any, Optional
from app.domain.repositories import UserRepository
from app.domain.exceptions import UnauthorizedError
from app.infrastructure.security.jwt import create_access_token, decode_access_token

class LoginUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str, password: str) -> Dict[str, Any]:
        user = self.user_repo.get_by_username(username)
        if not user:
            raise UnauthorizedError("Invalid username or password")

        # Verify password hash using bcrypt
        is_valid = bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
        if not is_valid:
            raise UnauthorizedError("Invalid username or password")

        # Create JWT access token with subject as user_id and username
        token_payload = {
            "sub": str(user.user_id),
            "username": user.username,
            "email": user.email
        }
        access_token = create_access_token(data=token_payload)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }


class LogoutUseCase:
    def execute(self, token: Optional[str]) -> Dict[str, str]:
        if not token:
            raise UnauthorizedError("Authorization token required for logout")

        # Remove "Bearer " prefix if provided
        clean_token = token.replace("Bearer ", "").strip()
        try:
            # Decode and verify token validity
            decode_access_token(clean_token)
        except Exception:
            raise UnauthorizedError("Invalid or expired token")

        return {"message": "Successfully logged out"}
