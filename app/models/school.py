from sqlalchemy.orm import Mapped

from app.models.base import Base


class School(Base):
    __tablename__ = "school"

    name: Mapped[str]
    initial: Mapped[str]
    arrival_time: Mapped[str]
    departure_time: Mapped[str]
    email: Mapped[str | None]

    def __repr__(self) -> str:
        return f"School: {self.name}"
