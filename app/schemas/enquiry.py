import enum

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, EmailStr

from app.schemas.base import BaseIn, BaseOut
from app.schemas.location import LocationOut
from app.schemas.school import SchoolOut


def validate_postal_code(postal_code: str) -> str:
    if postal_code and (len(postal_code) != 6 or not postal_code.isdigit()):
        raise ValueError("Postal code must be exactly 6 digits")
    return postal_code


class EnquiryStatus(enum.Enum):
    TBC = "To Be Confirmed"
    OPTION = "Option"
    SENT = "Enquiry Sent"
    REGISTRATION = "Registration"
    REJECTED = "Rejected"


PostalCode = Annotated[str, AfterValidator(validate_postal_code)]


class EnquiryBase(BaseIn):
    email: EmailStr
    block: str
    remark: str
    fare: int
    home_postal_code: PostalCode
    home_address: str
    home_unit_no: str
    am_postal_code: PostalCode
    am_address: str
    pm_postal_code: PostalCode
    pm_address: str
    school_id: UUID
    status: EnquiryStatus | None
    is_email_sent: bool
    is_favourite: bool
    am_location_id: UUID | None
    pm_location_id: UUID | None
    year: int
    am_icon: str
    pm_icon: str


class EnquiryCreate(BaseIn):
    email: EmailStr
    block: str = ""
    remark: str = ""
    fare: int = 0
    home_postal_code: PostalCode
    home_unit_no: str
    am_postal_code: PostalCode
    pm_postal_code: PostalCode
    school_id: UUID
    status: EnquiryStatus | None = None
    is_email_sent: bool = False
    is_favourite: bool = False
    am_location_id: UUID | None = None
    pm_location_id: UUID | None = None
    year: int
    am_icon: str = ""
    pm_icon: str = ""


class EnquiryUpdate(BaseIn):
    email: EmailStr | None = None
    block: str | None = None
    remark: str | None = None
    fare: int | None = None
    home_postal_code: PostalCode | None = None
    home_unit_no: str | None = None
    am_postal_code: PostalCode | None = None
    pm_postal_code: PostalCode | None = None
    status: EnquiryStatus | None = None
    is_email_sent: bool | None = None
    is_favourite: bool | None = None
    school_id: UUID | None = None
    am_location_id: UUID | None = None
    pm_location_id: UUID | None = None
    year: int | None = None
    am_icon: str | None = None
    pm_icon: str | None = None


class EnquiryOut(EnquiryBase, BaseOut):
    school: SchoolOut
    am_location: LocationOut | None
    pm_location: LocationOut | None
    created_on: datetime
