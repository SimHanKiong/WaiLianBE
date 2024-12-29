from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from psycopg import errors

from app.crud.base import ModelType


def raise_missing_exception(obj: ModelType | None, model: str):
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{model} not found."
        )
    return obj


def raise_database_exception(exc: IntegrityError, model: str):
    if isinstance(exc.orig, errors.ForeignKeyViolation):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A related record of {model} is missing.",
        )
    elif isinstance(exc.orig, errors.UniqueViolation):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Duplicate {model} detected.",
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="A database integrity error occurred.",
    )

