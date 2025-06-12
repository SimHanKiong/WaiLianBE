from fastapi import FastAPI

from app.api.main import api_router
from app.core.exception import (
    IntegrityException,
    UniqueViolationException,
    MissingRecordException,
)
from app.api.exception_handlers import (
    integrity_error_handler,
    unique_violation_error_handler,
    missing_record_error_handler,
)

app = FastAPI()

app.include_router(api_router)

app.add_exception_handler(IntegrityException, integrity_error_handler)
app.add_exception_handler(UniqueViolationException, unique_violation_error_handler)
app.add_exception_handler(MissingRecordException, missing_record_error_handler)
