class DomainException(Exception):
    """Base exception for domain business logic errors."""
    pass

class EntityNotFoundError(DomainException):
    """Raised when a requested entity does not exist in the system."""
    pass

class EntityAlreadyExistsError(DomainException):
    """Raised when attempting to create an entity that already exists (e.g. unique constraint violation)."""
    pass
