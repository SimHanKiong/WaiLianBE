import enum
from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.location import Location
from app.models.school import School


class EnquiryStatus(enum.Enum):
    TBC = "To Be Confirmed"
    SENT = "Enquiry Sent"
    RECEIVED = "Registration Received"


class Enquiry(Base):
    __tablename__ = "enquiry"

    date: Mapped[str]
    phone_no: Mapped[str]
    block: Mapped[str]
    remark: Mapped[str]
    fare: Mapped[int]
    status: Mapped[EnquiryStatus | None]

    school_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("school.id", ondelete="CASCADE")
    )
    school: Mapped[School | None] = relationship()

    am_location_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("location.id", ondelete="SET NULL")
    )
    am_location: Mapped[Location | None] = relationship(foreign_keys=[am_location_id])

    pm_location_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("location.id", ondelete="SET NULL")
    )
    pm_location: Mapped[Location | None] = relationship(foreign_keys=[pm_location_id])

    def __repr__(self) -> str:
        return f"Enquiry: {self.phone_no}"
