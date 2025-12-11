from fastapi import FastAPI

from app.api.exception_handlers import integrity_error_handler
from app.api.exception_handlers import missing_record_error_handler
from app.api.exception_handlers import unique_violation_error_handler
from app.api.main import api_router
from app.core.exception import IntegrityException
from app.core.exception import MissingRecordException
from app.core.exception import UniqueViolationException


app = FastAPI()

app.include_router(api_router)

app.add_exception_handler(IntegrityException, integrity_error_handler)
app.add_exception_handler(UniqueViolationException, unique_violation_error_handler)
app.add_exception_handler(MissingRecordException, missing_record_error_handler)
