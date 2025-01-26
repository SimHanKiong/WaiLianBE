from uuid import UUID
from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from app.core.exception import raise_database_exception, raise_missing_exception
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
    return raise_missing_exception(enquiry, "Enquiry")


@router.post("/", response_model=EnquiryOut)
def create_enquiry(db: SessionDep, enquiry_in: EnquiryCreate):
    try:
        enquiry = enquiry_crud.create(db, enquiry_in)
        return enquiry
    except IntegrityError as e:
        raise_database_exception(e, "Enquiry")


@router.patch("/{id:uuid}", response_model=EnquiryOut)
def update_enquiry(db: SessionDep, id: UUID, enquiry_in: EnquiryUpdate):
    try:
        enquiry = enquiry_crud.update(db, id, enquiry_in)
        return raise_missing_exception(enquiry, "Enquiry")
    except IntegrityError as e:
        raise_database_exception(e, "Enquiry")


@router.delete("/{id:uuid}", response_model=EnquiryOut)
def delete_enquiry(db: SessionDep, id: UUID):
    enquiry = enquiry_crud.delete(db, id)
    return raise_missing_exception(enquiry, "Enquiry")
