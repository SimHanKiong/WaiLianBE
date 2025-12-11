from fastapi import APIRouter

from app.api.routes import enquiry
from app.api.routes import file
from app.api.routes import location
from app.api.routes import parent
from app.api.routes import school


api_router = APIRouter()
api_router.include_router(school.router, prefix="/school", tags=["Schools"])
api_router.include_router(location.router, prefix="/location", tags=["Locations"])
api_router.include_router(enquiry.router, prefix="/enquiry", tags=["Enquiries"])
api_router.include_router(parent.router, prefix="/parent", tags=["Parents"])
api_router.include_router(file.router, prefix="/file", tags=["Files"])
