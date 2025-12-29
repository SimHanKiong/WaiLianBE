from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas import ParentCreate, ParentOut
from app.services import parent_service


router = APIRouter()


@router.post("/", response_model=ParentOut)
def create_parent(db: SessionDep, parent_in: ParentCreate):
    parent = parent_service.create_parent(db, parent_in)
    return parent
