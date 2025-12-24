from sqlalchemy.orm import Mapped

from app.models.base import Base


class Bus(Base):
    __tablename__ = "bus"

    name: Mapped[str]
    am_plate_no: Mapped[str]
    am_capacity: Mapped[int]
    pm_plate_no: Mapped[str]
    pm_capacity: Mapped[int]
    colour: Mapped[str]
