from uuid import UUID

from sqlalchemy.orm import Session

from app.core.email import send_enquiry_email
from app.core.external import get_address
from app.crud.enquiry import enquiry_crud
from app.schemas import EnquiryBase, EnquiryCreate, EnquiryOut, EnquiryUpdate


def read_enquiries(db: Session) -> list[EnquiryOut]:
    enquiries = enquiry_crud.read_all(db)
    return [EnquiryOut.model_validate(enquiry) for enquiry in enquiries]


def read_enquiry(db: Session, id: UUID) -> EnquiryOut | None:
    enquiry = enquiry_crud.read_one(db, enquiry_crud.model.id == id)
    return EnquiryOut.model_validate(enquiry)


def create_enquiry(db: Session, enquiry_in: EnquiryCreate) -> EnquiryOut:
    enquiry = EnquiryBase(
        **enquiry_in.model_dump(),
        home_address=get_address(enquiry_in.home_postal_code)
        if enquiry_in.home_postal_code
        else "",
        am_address=get_address(enquiry_in.am_postal_code)
        if enquiry_in.am_postal_code
        else "",
        pm_address=get_address(enquiry_in.pm_postal_code)
        if enquiry_in.pm_postal_code
        else "",
    )
    return EnquiryOut.model_validate(enquiry_crud.create(db, enquiry))


async def update_enquiry(
    db: Session, id: UUID, enquiry_in: EnquiryUpdate
) -> EnquiryOut | None:
    enquiry_dict = enquiry_in.model_dump(exclude_unset=True)
    if enquiry_in.home_postal_code:
        home_address = get_address(enquiry_in.home_postal_code)
        enquiry_dict["home_address"] = home_address

    if enquiry_in.am_postal_code:
        am_address = get_address(enquiry_in.am_postal_code)
        enquiry_dict["am_address"] = am_address

    if enquiry_in.pm_postal_code:
        pm_address = get_address(enquiry_in.pm_postal_code)
        enquiry_dict["pm_address"] = pm_address

    if enquiry_in.status:
        enquiry_dict["is_email_sent"] = False

    enquiry = enquiry_crud.update(db, id, enquiry_dict)
    if not enquiry:
        return None

    enquiry = EnquiryOut.model_validate(enquiry)
    if enquiry_in.is_email_sent:
        await send_enquiry_email(enquiry)
    
    return enquiry


def delete_enquiries(db: Session, ids: list[UUID]) -> list[EnquiryOut]:
    enquiries = enquiry_crud.delete_all(db, ids)
    return [EnquiryOut.model_validate(enquiry) for enquiry in enquiries]