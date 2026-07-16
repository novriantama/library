# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Request, status
# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware

# Database and ORM
from app.infrastructure.database import Base, engine
# Import ORM models to register them on the Base metadata
import app.infrastructure.orm  # noqa: F401

# Routers
from app.infrastructure.api.v1.authors import router as authors_router
from app.infrastructure.api.v1.books import router as books_router
from app.infrastructure.api.v1.book_authors import router as book_authors_router

# Domain Exceptions
from app.domain.exceptions import EntityNotFoundError, EntityAlreadyExistsError, DomainException

# Create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="Clean Architecture CRUD backend built with Python FastAPI",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers to map Domain Exceptions to HTTP Responses
@app.exception_handler(EntityNotFoundError)
def entity_not_found_handler(request: Request, exc: EntityNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )

@app.exception_handler(EntityAlreadyExistsError)
def entity_already_exists_handler(request: Request, exc: EntityAlreadyExistsError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

@app.exception_handler(DomainException)
def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

# Include API Routers under /api/v1 prefix
app.include_router(authors_router, prefix="/api/v1")
app.include_router(books_router, prefix="/api/v1")
app.include_router(book_authors_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Library Management API!",
        "docs_url": "/docs"
    }
