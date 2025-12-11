import enum

from datetime import date
from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator

from app.schemas.base import BaseIn
from app.schemas.base import BaseOut


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


class StudentGender(enum.Enum):
    MALE = "M"
    FEMALE = "F"


class TransportRequirement(enum.Enum):
    AM = "AM"
    PM = "PM"
    BOTH = "Both"


class StudentBase(BaseIn):
    full_name: str
    given_name: str
    gender: StudentGender
    level: Annotated[int, AfterValidator(validate_level)]
    class_name: str
    date_of_birth: date
    nric: Annotated[str, AfterValidator(validate_nric)]
    transport_start_date: date
    transport_requirement: TransportRequirement
    block: str
    status: str
    school_id: UUID
    am_location_id: UUID | None
    pm_location_id: UUID | None
    parent_id: UUID


class StudentCreateFromEnquiry(BaseIn):
    full_name: str
    given_name: str
    gender: StudentGender
    level: Annotated[int, AfterValidator(validate_level)]
    class_name: str
    date_of_birth: date
    nric: Annotated[str, AfterValidator(validate_nric)]
    transport_start_date: date
    transport_requirement: TransportRequirement


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
    pass
