import enum

from datetime import date
from typing import TYPE_CHECKING, Annotated, Optional
from uuid import UUID

from pydantic import AfterValidator


if TYPE_CHECKING:
    from app.schemas.location import LocationOut
    from app.schemas.parent import ParentOut

from app.schemas.base import BaseIn, BaseOut
from app.schemas.school import SchoolOut


def validate_level(level: int) -> int:
    if level < 1 or level > 6:
        raise ValueError("Level must be between 1 and 6")
    return level


def validate_nric(nric: str) -> str:
    if (
        len(nric) != 9
        or not nric[0].isalpha()
        or not nric[-1].isalpha()
        or not nric[1:-1].isdigit()
    ):
        raise ValueError("NRIC must be in the format of S1234567X")
    return nric


Level = Annotated[int, AfterValidator(validate_level)]
NRIC = Annotated[str, AfterValidator(validate_nric)]


class Gender(enum.Enum):
    MALE = "M"
    FEMALE = "F"


class TransportRequirement(enum.Enum):
    AM = "AM"
    PM = "PM"
    BOTH = "Both"


class StudentStatus(enum.Enum):
    PENDING = "Pending"
    NEW = "New"


class StudentBase(BaseIn):
    full_name: str
    given_name: str
    gender: Gender
    level: Level
    class_name: str
    date_of_birth: date
    nric: NRIC
    transport_start_date: date
    transport_requirement: TransportRequirement
    block: str
    status: StudentStatus | None
    am_icon: str
    pm_icon: str
    is_favourite: bool
    remark: str
    icon: str
    school_id: UUID
    am_location_id: UUID | None
    pm_location_id: UUID | None
    parent_id: UUID


class StudentCreate(BaseIn):
    full_name: str
    given_name: str
    gender: Gender
    level: Level
    class_name: str
    date_of_birth: date
    nric: NRIC
    transport_start_date: date
    transport_requirement: TransportRequirement
    block: str
    status: StudentStatus | None
    am_icon: str = ""
    pm_icon: str = ""
    is_favourite: bool = False
    remark: str = ""
    icon: str = ""
    school_id: UUID
    am_location_id: UUID
    pm_location_id: UUID


class StudentCreateFromEnquiry(BaseIn):
    full_name: str
    given_name: str
    gender: Gender
    level: Level
    class_name: str
    date_of_birth: date
    nric: NRIC
    transport_start_date: date
    transport_requirement: TransportRequirement
    am_icon: str = ""
    pm_icon: str = ""
    is_favourite: bool = False
    remark: str = ""
    icon: str = ""


class StudentUpdate(BaseIn):
    block: str | None = None
    am_icon: str | None = None
    pm_icon: str | None = None
    is_favourite: bool | None = None
    remark: str | None = None
    icon: str | None = None
    am_location_id: UUID | None = None
    pm_location_id: UUID | None = None


# class StudentUpdate(StudentBase):
#     full_name: str | None = None
#     given_name: str | None = None
#     gender: StudentGender | None = None
#     level: Annotated[int, AfterValidator(validate_level)] | None = None
#     class_name: str | None = None
#     date_of_birth: date | None = None
#     nric: Annotated[str, AfterValidator(validate_nric)] | None = None
#     transport_start_date: date | None = None
#     transport_requirement: TransportRequirement | None = None
#     block: str | None = None
#     status: str | None = None
#     school_id: UUID | None = None
#     am_location_id: UUID | None = None
#     pm_location_id: UUID | None = None
#     parent_id: UUID | None = None


class StudentOut(StudentBase, BaseOut):
    order: int = 0
    school: SchoolOut
    am_location: Optional["LocationOut"]
    pm_location: Optional["LocationOut"]


class StudentOutExtended(StudentOut):
    parent: "ParentOut"
