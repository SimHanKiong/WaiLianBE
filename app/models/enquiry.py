import enum
from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.location import Location
from app.models.school import School


class EnquiryStatus(enum.Enum):
    TBC = "To Be Confirmed"
    OPTION = "Option"
    SENT = "Enquiry Sent"
    REGISTRATION = "Registration"
    REJECTED = "Rejected"


class Enquiry(Base):
    __tablename__ = "enquiry"

    email: Mapped[str]
    block: Mapped[str]
    remark: Mapped[str]
    fare: Mapped[int]
    home_postal_code: Mapped[str]
    home_unit_no: Mapped[str]
    home_address: Mapped[str]
    am_postal_code: Mapped[str]
    am_address: Mapped[str]
    pm_postal_code: Mapped[str]
    pm_address: Mapped[str]
    year: Mapped[int]
    status: Mapped[EnquiryStatus | None]
    email_sent: Mapped[bool]

    school_id: Mapped[UUID] = mapped_column(
        ForeignKey("school.id", ondelete="CASCADE")
    )
    school: Mapped[School] = relationship()

    am_location_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("location.id", ondelete="SET NULL")
    )
    am_location: Mapped[Location | None] = relationship(foreign_keys=[am_location_id])

    pm_location_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("location.id", ondelete="SET NULL")
    )
    pm_location: Mapped[Location | None] = relationship(foreign_keys=[pm_location_id])

    def __repr__(self) -> str:
        return f"Enquiry: {self.email}"
