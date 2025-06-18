from uuid import UUID
from sqlalchemy.orm import Session


from app.core.external import get_address
from app.crud.base import CRUDBase
from app.models import Enquiry
from app.schemas.enquiry import EnquiryCreate, EnquiryUpdate


class CRUDEnquiry(CRUDBase[Enquiry]):
    def create(self, db: Session, enquiry_in: EnquiryCreate) -> Enquiry:
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
        return super().create(db, enquiry_dict)

    def update(self, db: Session, id: UUID, enquiry_in: EnquiryUpdate) -> Enquiry:
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

        return super().update(db, id, enquiry_dict)


enquiry_crud = CRUDEnquiry(model=Enquiry)
