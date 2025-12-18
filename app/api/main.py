from fastapi import APIRouter

from app.api.routes import enquiry, file, location, parent, school, student


api_router = APIRouter()
api_router.include_router(school.router, prefix="/school", tags=["Schools"])
api_router.include_router(location.router, prefix="/location", tags=["Locations"])
api_router.include_router(enquiry.router, prefix="/enquiry", tags=["Enquiries"])
api_router.include_router(parent.router, prefix="/parent", tags=["Parents"])
api_router.include_router(student.router, prefix="/student", tags=["Students"])
api_router.include_router(file.router, prefix="/file", tags=["Files"])
