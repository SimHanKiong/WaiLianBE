from fastapi import APIRouter

from app.api.routes import school

api_router = APIRouter()
api_router.include_router(school.router, prefix="/school", tags=["Schools"])
