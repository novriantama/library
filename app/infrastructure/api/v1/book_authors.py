from typing import List, Optional
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.infrastructure.api.schemas.book_author import (
    BookAuthorCreate,
    BookAuthorUpdate,
    BookAuthorResponse,
)
from app.infrastructure.api.dependencies import (
    get_assign_author_to_book_use_case,
    get_update_book_author_role_use_case,
    get_remove_author_from_book_use_case,
    get_get_book_authors_use_case,
)
from app.use_cases.book_author import (
    AssignAuthorToBookUseCase,
    UpdateBookAuthorRoleUseCase,
    RemoveAuthorFromBookUseCase,
    GetBookAuthorsUseCase,
)

router = APIRouter(prefix="/book-authors", tags=["Book Authors"])

@router.post("/", response_model=BookAuthorResponse, status_code=status.HTTP_201_CREATED)
def assign_author_to_book(
    payload: BookAuthorCreate,
    assign_use_case: AssignAuthorToBookUseCase = Depends(get_assign_author_to_book_use_case),
):
    return assign_use_case.execute(
        book_id=payload.book_id,
        author_id=payload.author_id,
        role=payload.role,
    )

@router.get("/", response_model=List[BookAuthorResponse])
def list_book_authors(
    book_id: Optional[int] = Query(None, description="Filter by Book ID"),
    author_id: Optional[int] = Query(None, description="Filter by Author ID"),
    get_use_case: GetBookAuthorsUseCase = Depends(get_get_book_authors_use_case),
):
    if book_id is not None:
        return get_use_case.get_by_book_id(book_id)
    if author_id is not None:
        return get_use_case.get_by_author_id(author_id)
    return get_use_case.get_all()

@router.get("/{book_id}/{author_id}", response_model=BookAuthorResponse)
def get_book_author_relationship(
    book_id: int,
    author_id: int,
    get_use_case: GetBookAuthorsUseCase = Depends(get_get_book_authors_use_case),
):
    relationship = get_use_case.get_by_ids(book_id, author_id)
    if not relationship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relationship between book_id {book_id} and author_id {author_id} not found",
        )
    return relationship

@router.put("/{book_id}/{author_id}", response_model=BookAuthorResponse)
def update_book_author_role(
    book_id: int,
    author_id: int,
    payload: BookAuthorUpdate,
    update_use_case: UpdateBookAuthorRoleUseCase = Depends(get_update_book_author_role_use_case),
):
    return update_use_case.execute(
        book_id=book_id,
        author_id=author_id,
        role=payload.role,
    )

@router.delete("/{book_id}/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_author_from_book(
    book_id: int,
    author_id: int,
    remove_use_case: RemoveAuthorFromBookUseCase = Depends(get_remove_author_from_book_use_case),
):
    remove_use_case.execute(book_id, author_id)
