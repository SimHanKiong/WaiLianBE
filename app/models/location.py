from sqlalchemy.orm import Mapped, mapped_column
import datetime

from app.models.base import Base
from app.models.route import RouteType


class Location(Base):
    __tablename__ = "location"

    address: Mapped[str] = mapped_column(nullable=False)
    time: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[RouteType] = mapped_column(nullable=False)
    time_reached: Mapped[datetime.time] = mapped_column(nullable=True)
    position: Mapped[float] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"Location: {self.address}, {self.type}"
