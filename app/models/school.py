from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class School(Base):
    __tablename__ = "school"

    name: Mapped[str] = mapped_column(nullable=False)
    initial: Mapped[str] = mapped_column(nullable=False)
    arrival_time: Mapped[str] = mapped_column(nullable=False)
    departure_time: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"School: {self.name}"
