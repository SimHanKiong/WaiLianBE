from uuid import UUID

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.core.exception import MissingRecordException
from app.schemas import (
    ParentCreate,
    ParentCreateFromEnquiry,
    ParentOut,
    ParentOutExtended,
    ParentUpdate,
)
from app.services import parent_service


router = APIRouter()


@router.get("/{id:uuid}", response_model=ParentOutExtended)
def read_parent(db: SessionDep, id: UUID):
    parent = parent_service.read_parent(db, id)
    if not parent:
        raise MissingRecordException("Parent")
    return parent


@router.post("/", response_model=ParentOut)
def create_parent(db: SessionDep, parent_in: ParentCreate):
    parent = parent_service.create_parent(db, parent_in)
    return parent


@router.post("/enquiry", response_model=ParentOut)
def create_parent_from_enquiry(db: SessionDep, parent_in: ParentCreateFromEnquiry):
    parent = parent_service.create_parent_from_enquiry(db, parent_in)
    return parent


@router.patch("/{id:uuid}", response_model=ParentOut)
def update_parent(db: SessionDep, id: UUID, parent_in: ParentUpdate):
    parent = parent_service.update_parent(db, id, parent_in)
    if not parent:
        raise MissingRecordException("Parent")
    return parent
