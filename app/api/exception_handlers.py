from fastapi import HTTPException, Request, status

from app.core.exception import (
    IntegrityException,
    MissingRecordException,
)


def integrity_error_handler(_: Request, e: IntegrityException):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(e),
    )


def missing_record_error_handler(_: Request, e: MissingRecordException):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(e),
    )
