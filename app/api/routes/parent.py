from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas import ParentCreate, ParentOutWithChildren
from app.services import parent as parent_service


router = APIRouter()


@router.post("/", response_model=ParentOutWithChildren)
def create_parent(db: SessionDep, parent_in: ParentCreate):
    parent = parent_service.create_parent(db, parent_in)
    return parent
