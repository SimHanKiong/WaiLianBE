from uuid import UUID
from fastapi import APIRouter

from app.core.exception import MissingRecordException
from app.schemas.enquiry import EnquiryCreate, EnquiryOut, EnquiryUpdate
from app.crud.enquiry import enquiry_crud
from app.api.deps import SessionDep


router = APIRouter()


@router.get("/", response_model=list[EnquiryOut])
def read_enquiries(db: SessionDep):
    enquiries = enquiry_crud.read_all(db)
    return enquiries


@router.get("/{id:uuid}", response_model=EnquiryOut)
def read_enquiry(db: SessionDep, id: UUID):
    enquiry = enquiry_crud.read_one(db, enquiry_crud.model.id == id)
    if not enquiry:
        raise MissingRecordException("Enquiry")
    return enquiry


@router.post("/", response_model=EnquiryOut)
def create_enquiry(db: SessionDep, enquiry_in: EnquiryCreate):
    enquiry = enquiry_crud.create(db, enquiry_in)
    return enquiry


@router.patch("/{id:uuid}", response_model=EnquiryOut)
def update_enquiry(db: SessionDep, id: UUID, enquiry_in: EnquiryUpdate):
    enquiry = enquiry_crud.update(db, id, enquiry_in)
    if not enquiry:
        raise MissingRecordException("Enquiry")
    return enquiry


@router.delete("/{id:uuid}", response_model=EnquiryOut)
def delete_enquiry(db: SessionDep, id: UUID):
    enquiry = enquiry_crud.delete(db, id)
    if not enquiry:
        raise MissingRecordException("Enquiry")
    return enquiry
