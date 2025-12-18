from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.models.parent import Parent

from app.models.base import Base
from app.models.location import Location
from app.models.school import School


class Student(Base):
    __tablename__ = "student"

    full_name: Mapped[str]
    given_name: Mapped[str]
    gender: Mapped[str]
    level: Mapped[int]
    class_name: Mapped[str]
    date_of_birth: Mapped[date]
    nric: Mapped[str]
    transport_start_date: Mapped[date]
    transport_requirement: Mapped[str]
    block: Mapped[str]
    status: Mapped[str]

    school_id: Mapped[UUID] = mapped_column(ForeignKey("school.id", ondelete="CASCADE"))
    school: Mapped[School] = relationship()

    am_location_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("location.id", ondelete="SET NULL")
    )
    am_location: Mapped[Location | None] = relationship(foreign_keys=[am_location_id])

    pm_location_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("location.id", ondelete="SET NULL")
    )
    pm_location: Mapped[Location | None] = relationship(foreign_keys=[pm_location_id])

    parent_id: Mapped[UUID] = mapped_column(ForeignKey("parent.id", ondelete="CASCADE"))
    parent: Mapped["Parent"] = relationship(back_populates="children")

    def __repr__(self) -> str:
        return f"Student: {self.full_name}"
