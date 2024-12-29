from uuid import UUID
from app.models.enquiry import EnquiryStatus
from app.schemas.location import LocationOut
from app.schemas.school import SchoolOut
from app.schemas.base import BaseOut, BaseIn


class EnquiryBase(BaseIn):
    date: str
    phone_no: str
    block: str
    remark: str
    fare: int
    status: EnquiryStatus | None
    school_id: UUID | None
    am_location_id: UUID | None
    pm_location_id: UUID | None


class EnquiryCreate(EnquiryBase):
    pass


class EnquiryUpdate(EnquiryBase):
    date: str | None = None
    phone_no: str | None = None
    block: str | None = None
    remark: str | None = None
    fare: int | None = None
    status: EnquiryStatus | None = None
    school_id: UUID | None = None
    am_location_id: UUID | None = None
    pm_location_id: UUID | None = None


class EnquiryOut(EnquiryBase, BaseOut):
    school: SchoolOut | None
    am_location: LocationOut | None
    pm_location: LocationOut | None
