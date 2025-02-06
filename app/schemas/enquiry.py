from uuid import UUID
from pydantic import EmailStr, field_validator

from app.models.enquiry import EnquiryStatus
from app.schemas.location import LocationOut
from app.schemas.school import SchoolOut
from app.schemas.base import BaseOut, BaseIn


class EnquiryBase(BaseIn):
    email: EmailStr
    block: str
    remark: str
    fare: int
    home_postal_code: str
    home_unit_no: str
    am_postal_code: str
    pm_postal_code: str
    school_id: UUID
    status: EnquiryStatus | None
    am_location_id: UUID | None
    pm_location_id: UUID | None
    year: int

    @field_validator("home_postal_code", "am_postal_code", "pm_postal_code")
    def validate_postal_code(cls, v: str) -> str:
        if v and (len(v) != 6 or not v.isdigit()):
            raise ValueError("Postal code must be exactly 6 digits")
        return v


class EnquiryCreate(EnquiryBase):
    pass


class EnquiryUpdate(EnquiryBase):
    email: EmailStr | None = None
    block: str | None = None
    remark: str | None = None
    fare: int | None = None
    home_postal_code: str | None = None
    home_unit_no: str | None = None
    am_postal_code: str | None = None
    pm_postal_code: str | None = None
    status: EnquiryStatus | None = None
    school_id: UUID | None = None
    am_location_id: UUID | None = None
    pm_location_id: UUID | None = None
    year: int | None = None


class EnquiryOut(EnquiryBase, BaseOut):
    school: SchoolOut | None
    am_location: LocationOut | None
    pm_location: LocationOut | None
    home_address: str
    am_address: str
    pm_address: str
