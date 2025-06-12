from fastapi import Request, HTTPException, status
from app.core.exception import (
    IntegrityException,
    UniqueViolationException,
    MissingRecordException,
)


def integrity_error_handler(_: Request, e: IntegrityException):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e),
    )


def unique_violation_error_handler(_: Request, e: UniqueViolationException):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e),
    )


def missing_record_error_handler(_: Request, e: MissingRecordException):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(e),
    )
