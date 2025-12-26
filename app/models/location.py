import datetime

from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.bus import Bus
from app.models.route import RouteType


class Location(Base):
    __tablename__ = "location"

    address: Mapped[str]
    time: Mapped[str]
    type: Mapped[RouteType]

    bus_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("bus.id", ondelete="SET NULL")
    )
    bus: Mapped[Bus | None] = relationship()

    __table_args__ = (UniqueConstraint("address", "type", name="uq_address_type"),)

    def __repr__(self) -> str:
        return f"Location: {self.address}, {self.type}"
