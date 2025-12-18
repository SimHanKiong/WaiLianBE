from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.models.student import Student

from app.models.base import Base
from app.models.enquiry import Enquiry
from app.models.student import Student


class Parent(Base):
    __tablename__ = "parent"

    email: Mapped[str]
    contact1_name: Mapped[str]
    contact1_no: Mapped[str]
    contact1_relationship: Mapped[str]
    contact2_name: Mapped[str]
    contact2_no: Mapped[str]
    contact2_relationship: Mapped[str]
    home_postal_code: Mapped[str]
    home_unit_no: Mapped[str]
    home_address: Mapped[str]
    am_postal_code: Mapped[str]
    am_address: Mapped[str]
    pm_postal_code: Mapped[str]
    pm_address: Mapped[str]
    under_fas: Mapped[bool]
    fare: Mapped[int]

    enquiry_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("enquiry.id", ondelete="Set NULL")
    )
    enquiry: Mapped[Enquiry | None] = relationship()

    children: Mapped[list["Student"]] = relationship(back_populates="parent")

    def __repr__(self) -> str:
        return f"Parent: {self.contact1_name}, {self.email}"
