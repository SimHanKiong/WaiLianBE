from uuid import UUID

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.core.email import send_enquiry_email
from app.core.exception import MissingRecordException
from app.schemas import EnquiryCreate, EnquiryOut, EnquiryUpdate
from app.services import enquiry as enquiry_service


router = APIRouter()


@router.get("/", response_model=list[EnquiryOut])
def read_enquiries(db: SessionDep):
    enquiries = enquiry_service.read_enquiries(db)
    return enquiries


@router.get("/{id:uuid}", response_model=EnquiryOut)
def read_enquiry(db: SessionDep, id: UUID):
    enquiry = enquiry_service.read_enquiry(db, id)
    if not enquiry:
        raise MissingRecordException("Enquiry")
    return enquiry


@router.post("/", response_model=EnquiryOut)
def create_enquiry(db: SessionDep, enquiry_in: EnquiryCreate):
    enquiry = enquiry_service.create_enquiry(db, enquiry_in)
    return enquiry


@router.patch("/{id:uuid}", response_model=EnquiryOut)
async def update_enquiry(db: SessionDep, id: UUID, enquiry_in: EnquiryUpdate):
    enquiry = await enquiry_service.update_enquiry(db, id, enquiry_in)
    if not enquiry:
        raise MissingRecordException("Enquiry")
    return enquiry


@router.delete("/", response_model=list[EnquiryOut])
def delete_enquiries(db: SessionDep, ids: list[UUID]):
    enquiries = enquiry_service.delete_enquiries(db, ids)
    return enquiries
