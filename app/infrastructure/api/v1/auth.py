from typing import Optional
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, Header, status
from app.infrastructure.api.schemas.auth import UserLogin, TokenResponse, LogoutResponse
from app.infrastructure.api.dependencies import get_login_use_case, get_logout_use_case
from app.use_cases.auth import LoginUseCase, LogoutUseCase

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    payload: UserLogin,
    login_use_case: LoginUseCase = Depends(get_login_use_case),
):
    return login_use_case.execute(
        username=payload.username,
        password=payload.password,
    )

@router.post("/logout", response_model=LogoutResponse, status_code=status.HTTP_200_OK)
def logout(
    authorization: Optional[str] = Header(None),
    logout_use_case: LogoutUseCase = Depends(get_logout_use_case),
):
    return logout_use_case.execute(token=authorization)
