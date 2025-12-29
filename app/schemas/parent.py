from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import EmailStr


if TYPE_CHECKING:
    from app.schemas.student import StudentOut

from app.schemas.base import BaseIn, BaseOut
from app.schemas.student import StudentCreate


class ParentBase(BaseIn):
    email: EmailStr
    contact1_name: str
    contact1_no: str
    contact1_relationship: str
    contact2_name: str
    contact2_no: str
    contact2_relationship: str
    home_postal_code: str
    home_unit_no: str
    home_address: str
    am_postal_code: str
    am_address: str
    pm_postal_code: str
    pm_address: str
    under_fas: bool
    fare: int
    enquiry_id: UUID | None


class ParentCreate(BaseIn):
    contact1_name: str
    contact1_no: str
    contact1_relationship: str
    contact2_name: str
    contact2_no: str
    contact2_relationship: str
    under_fas: bool
    enquiry_id: UUID
    children: list[StudentCreate]


class ParentUpdate(ParentBase):
    email: EmailStr | None = None
    contact1_name: str | None = None
    contact1_no: str | None = None
    contact1_relationship: str | None = None
    contact2_name: str | None = None
    contact2_no: str | None = None
    contact2_relationship: str | None = None
    home_postal_code: str | None = None
    home_unit_no: str | None = None
    home_address: str | None = None
    am_postal_code: str | None = None
    am_address: str | None = None
    pm_postal_code: str | None = None
    pm_address: str | None = None
    under_fas: bool | None = None
    fare: int | None = None
    enquiry_id: UUID | None = None


class ParentOut(ParentBase, BaseOut):
    pass


class ParentOutExtended(ParentOut):
    children: list["StudentOut"]
