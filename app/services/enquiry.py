from uuid import UUID
from sqlalchemy.orm import Session


from app.core.external import get_address
from app.crud.enquiry import enquiry_crud
from app.schemas.enquiry import EnquiryCreate, EnquiryOut, EnquiryUpdate


def read_enquiries(db: Session) -> list[EnquiryOut]:
    enquiries = enquiry_crud.read_all(db)
    return enquiries


def read_enquiry(db: Session) -> EnquiryOut | None:
    enquiry = enquiry_crud.read_one(db, enquiry_crud.model.id == id)
    return enquiry


def create_enquiry(db: Session, enquiry_in: EnquiryCreate) -> EnquiryOut:
    enquiry_dict = enquiry_in.model_dump(exclude_none=True, exclude_unset=True)
    home_address = get_address(enquiry_in.home_postal_code)
    am_address = (
        get_address(enquiry_in.am_postal_code) if enquiry_in.am_postal_code else ""
    )
    pm_address = (
        get_address(enquiry_in.pm_postal_code) if enquiry_in.pm_postal_code else ""
    )
    enquiry_dict.update(
        {
            "home_address": home_address,
            "am_address": am_address,
            "pm_address": pm_address,
        }
    )
    return enquiry_crud.create(db, enquiry_dict)


def update_enquiry(
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

    return enquiry_crud.update(db, id, enquiry_dict)


def delete_enquiry(db: Session, id: UUID) -> EnquiryOut | None:
    enqiry = enquiry_crud.delete(db, id)
    return enqiry
