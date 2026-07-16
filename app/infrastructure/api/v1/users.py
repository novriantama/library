from typing import List
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.api.schemas.user import UserCreate, UserUpdate, UserResponse
from app.infrastructure.api.dependencies import (
    get_create_user_use_case,
    get_get_user_use_case,
    get_update_user_use_case,
    get_delete_user_use_case,
)
from app.use_cases.user import (
    CreateUserUseCase,
    GetUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
)

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    create_use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    return create_use_case.execute(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        user_id=payload.user_id,
    )

@router.get("/", response_model=List[UserResponse])
def list_users(
    get_use_case: GetUserUseCase = Depends(get_get_user_use_case),
):
    return get_use_case.get_all()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    get_use_case: GetUserUseCase = Depends(get_get_user_use_case),
):
    user = get_use_case.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdate,
    update_use_case: UpdateUserUseCase = Depends(get_update_user_use_case),
):
    return update_use_case.execute(
        user_id=user_id,
        username=payload.username,
        email=payload.email,
        password=payload.password,
    )

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    delete_use_case: DeleteUserUseCase = Depends(get_delete_user_use_case),
):
    delete_use_case.execute(user_id)
