import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped

from app.models.base import Base
from app.models.route import RouteType


class Location(Base):
    __tablename__ = "location"

    address: Mapped[str]
    time: Mapped[str]
    type: Mapped[RouteType]
    time_reached: Mapped[datetime.time | None]
    position: Mapped[float | None]

    __table_args__ = (UniqueConstraint("address", "type", name="uq_address_type"),)

    def __repr__(self) -> str:
        return f"Location: {self.address}, {self.type}"
