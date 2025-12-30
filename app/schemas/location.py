import enum

from collections import defaultdict
from datetime import time
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field, computed_field

from app.schemas.base import BaseIn, BaseOut
from app.schemas.bus import BusOut


if TYPE_CHECKING:
    from app.schemas.student import StudentOutExtended


class LocationType(enum.Enum):
    AM = "AM"
    PM = "PM"


class LocationBase(BaseIn):
    address: str
    time_reach: time
    type: LocationType
    bus_id: UUID | None


class LocationCreate(LocationBase):
    bus_id: UUID | None = None


class LocationUpdate(LocationBase):
    address: str | None = None
    time_reach: time | None = None
    type: LocationType | None = None
    bus_id: UUID | None = None


class LocationOut(LocationBase, BaseOut):
    bus: BusOut | None


class LocationOutExtended(LocationOut):
    am_students: list["StudentOutExtended"] = Field(exclude=True)
    pm_students: list["StudentOutExtended"] = Field(exclude=True)

    @computed_field
    @property
    def students(self) -> list["StudentOutExtended"]:
        students = (
            self.am_students if self.type == LocationType.AM else self.pm_students
        )
        parents: defaultdict[UUID, list[StudentOutExtended]] = defaultdict(list)
        for student in students:
            parents[student.parent_id].append(student)
        result = []
        for students in parents.values():
            for i, student in enumerate(
                sorted(students, key=lambda s: s.level, reverse=True)
            ):
                if len(students) == 1:
                    continue
                student.order = i + 1
            result.extend(students)
        return result
