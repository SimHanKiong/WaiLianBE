from fastapi import APIRouter

from app.api.deps import SessionDep
from app.schemas import ParentCreate, ParentCreateFromEnquiry, ParentOut
from app.services import parent_service


router = APIRouter()


@router.post("/", response_model=ParentOut)
def create_parent(db: SessionDep, parent_in: ParentCreate):
    parent = parent_service.create_parent(db, parent_in)
    return parent


@router.post("/enquiry", response_model=ParentOut)
def create_parent_from_enquiry(db: SessionDep, parent_in: ParentCreateFromEnquiry):
    parent = parent_service.create_parent_from_enquiry(db, parent_in)
    return parent
