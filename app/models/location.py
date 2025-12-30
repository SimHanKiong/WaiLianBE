from datetime import time
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.bus import Bus
from app.models.student import Student


if TYPE_CHECKING:
    from app.models.student import Student


class Location(Base):
    __tablename__ = "location"

    address: Mapped[str]
    time_reach: Mapped[time]
    type: Mapped[str]

    bus_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("bus.id", ondelete="SET NULL")
    )
    bus: Mapped[Bus | None] = relationship()

    am_students: Mapped[list["Student"]] = relationship(
        foreign_keys="Student.am_location_id", back_populates="am_location"
    )
    pm_students: Mapped[list["Student"]] = relationship(
        foreign_keys="Student.pm_location_id", back_populates="pm_location"
    )

    __table_args__ = (UniqueConstraint("address", "type", name="uq_address_type"),)

    def __repr__(self) -> str:
        return f"Location: {self.address}, {self.type}"
