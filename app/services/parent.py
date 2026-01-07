from sqlalchemy.orm import Session

from app.core.exception import IntegrityException
from app.core.external import get_address
from app.crud.enquiry import enquiry_crud
from app.crud.parent import parent_crud
from app.crud.student import student_crud
from app.schemas import (
    ParentBase,
    ParentCreate,
    ParentCreateFromEnquiry,
    ParentOut,
    StudentBase,
)
from app.schemas.student import StudentStatus


def create_parent(db: Session, parent_in: ParentCreate) -> ParentOut:
    parent = ParentBase(
        **parent_in.model_dump(),
        home_address=get_address(parent_in.home_postal_code)
        if parent_in.home_postal_code
        else "",
        am_address=get_address(parent_in.am_postal_code)
        if parent_in.am_postal_code
        else "",
        pm_address=get_address(parent_in.pm_postal_code)
        if parent_in.pm_postal_code
        else "",
        enquiry_id=None,
    )
    parent = parent_crud.create(db, parent)

    for child_in in parent_in.children:
        student = StudentBase(
            **child_in.model_dump(),
            parent_id=parent.id,
        )
        student_crud.create(db, student)

    return ParentOut.model_validate(parent)


def create_parent_from_enquiry(
    db: Session, parent_in: ParentCreateFromEnquiry
) -> ParentOut:
    enquiry = enquiry_crud.read_one(db, enquiry_crud.model.id == parent_in.enquiry_id)
    if not enquiry:
        raise IntegrityException("Enquiry")

    parent = ParentBase(
        **parent_in.model_dump(),
        email=enquiry.email,
        home_postal_code=enquiry.home_postal_code,
        home_unit_no=enquiry.home_unit_no,
        home_address=enquiry.home_address,
        am_postal_code=enquiry.am_postal_code,
        am_address=enquiry.am_address,
        pm_postal_code=enquiry.pm_postal_code,
        pm_address=enquiry.pm_address,
        fare=enquiry.fare,
    )
    parent = parent_crud.create(db, parent)

    for child_in in parent_in.children:
        student = StudentBase(
            **child_in.model_dump(),
            block=enquiry.block,
            status=StudentStatus.PENDING,
            school_id=enquiry.school_id,
            am_location_id=enquiry.am_location_id,
            pm_location_id=enquiry.pm_location_id,
            parent_id=parent.id,
        )
        student_crud.create(db, student)

    return ParentOut.model_validate(parent)
