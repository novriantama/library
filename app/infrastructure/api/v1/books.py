from typing import List
# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException, status
from app.infrastructure.api.schemas.book import BookCreate, BookUpdate, BookResponse
from app.infrastructure.api.dependencies import (
    get_create_book_use_case,
    get_get_book_use_case,
    get_update_book_use_case,
    get_delete_book_use_case,
)
from app.use_cases.book import (
    CreateBookUseCase,
    GetBookUseCase,
    UpdateBookUseCase,
    DeleteBookUseCase,
)

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: BookCreate,
    create_use_case: CreateBookUseCase = Depends(get_create_book_use_case),
):
    return create_use_case.execute(
        isbn=book_in.isbn,
        title=book_in.title,
        genre=book_in.genre,
        publish_date=book_in.publish_date,
        book_id=book_in.book_id,
    )

@router.get("/", response_model=List[BookResponse])
def list_books(
    get_use_case: GetBookUseCase = Depends(get_get_book_use_case),
):
    return get_use_case.get_all()

@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    get_use_case: GetBookUseCase = Depends(get_get_book_use_case),
):
    book = get_use_case.get_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book_in: BookUpdate,
    update_use_case: UpdateBookUseCase = Depends(get_update_book_use_case),
):
    return update_use_case.execute(
        book_id=book_id,
        isbn=book_in.isbn,
        title=book_in.title,
        genre=book_in.genre,
        publish_date=book_in.publish_date,
    )

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    delete_use_case: DeleteBookUseCase = Depends(get_delete_book_use_case),
):
    delete_use_case.execute(book_id)
