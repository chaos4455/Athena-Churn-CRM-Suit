from fastapi import HTTPException, status


class AthenaCRMException(Exception):
    """Base exception for Athena CRM."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EntityNotFoundException(AthenaCRMException):
    pass


class DuplicateEntityException(AthenaCRMException):
    pass


class InvalidOperationException(AthenaCRMException):
    pass


# HTTP helpers
def not_found(entity: str, id: str | int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} with id '{id}' not found.",
    )


def bad_request(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def conflict(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
