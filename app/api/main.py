from fastapi import APIRouter

from app.api.routes import school, location, enquiry

api_router = APIRouter()
api_router.include_router(school.router, prefix="/school", tags=["Schools"])
api_router.include_router(location.router, prefix="/location", tags=["Locations"])
api_router.include_router(enquiry.router, prefix="/enquiry", tags=["Enquiries"])
