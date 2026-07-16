from typing import List
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.api.schemas.author import AuthorCreate, AuthorUpdate, AuthorResponse
from app.infrastructure.api.dependencies import (
    get_create_author_use_case,
    get_get_author_use_case,
    get_update_author_use_case,
    get_delete_author_use_case,
)
from app.use_cases.author import (
    CreateAuthorUseCase,
    GetAuthorUseCase,
    UpdateAuthorUseCase,
    DeleteAuthorUseCase,
)

router = APIRouter(prefix="/author", tags=["Authors"])

@router.post("/", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def create_author(
    author_in: AuthorCreate,
    create_use_case: CreateAuthorUseCase = Depends(get_create_author_use_case),
):
    return create_use_case.execute(
        first_name=author_in.first_name,
        last_name=author_in.last_name,
        author_id=author_in.author_id,
    )

@router.get("/", response_model=List[AuthorResponse])
def list_authors(
    get_use_case: GetAuthorUseCase = Depends(get_get_author_use_case),
):
    return get_use_case.get_all()

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(
    author_id: int,
    get_use_case: GetAuthorUseCase = Depends(get_get_author_use_case),
):
    author = get_use_case.get_by_id(author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Author with id {author_id} not found",
        )
    return author

@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(
    author_id: int,
    author_in: AuthorUpdate,
    update_use_case: UpdateAuthorUseCase = Depends(get_update_author_use_case),
):
    # Exception handling for EntityNotFoundError is handled globally in main.py,
    # but let's be explicit if needed, or rely on global handler. Let's rely on global.
    return update_use_case.execute(
        author_id=author_id,
        first_name=author_in.first_name,
        last_name=author_in.last_name,
    )

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(
    author_id: int,
    delete_use_case: DeleteAuthorUseCase = Depends(get_delete_author_use_case),
):
    delete_use_case.execute(author_id)
