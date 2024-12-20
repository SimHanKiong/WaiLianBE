from fastapi import APIRouter

from app.api.routes import school, location

api_router = APIRouter()
api_router.include_router(school.router, prefix="/school", tags=["Schools"])
api_router.include_router(location.router, prefix="/location", tags=["Locations"])
