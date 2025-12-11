from sqlalchemy.orm import Session

from app.core.exception import IntegrityException
from app.crud.enquiry import enquiry_crud
from app.crud.parent import parent_crud
from app.crud.student import student_crud
from app.schemas.parent import ParentBase
from app.schemas.parent import ParentCreate
from app.schemas.parent import ParentOutWithChildren
from app.schemas.student import StudentBase


def create_parent(db: Session, parent_in: ParentCreate) -> ParentOutWithChildren:
    enquiry = enquiry_crud.read_one(db, enquiry_crud.model.id == parent_in.enquiry_id)
    if not enquiry:
        raise IntegrityException("Enquiry")

    parent = ParentBase(
        email=enquiry.email,
        contact1_name=parent_in.contact1_name,
        contact1_no=parent_in.contact1_no,
        contact1_relationship=parent_in.contact1_relationship,
        contact2_name=parent_in.contact2_name,
        contact2_no=parent_in.contact2_no,
        contact2_relationship=parent_in.contact2_relationship,
        home_postal_code=enquiry.home_postal_code,
        home_unit_no=enquiry.home_unit_no,
        home_address=enquiry.home_address,
        am_postal_code=enquiry.am_postal_code,
        am_address=enquiry.am_address,
        pm_postal_code=enquiry.pm_postal_code,
        pm_address=enquiry.pm_address,
        under_fas=parent_in.under_fas,
        fare=enquiry.fare,
        enquiry_id=enquiry.id,
    )
    parent = parent_crud.create(db, parent)

    for child_in in parent_in.children:
        student = StudentBase(
            full_name=child_in.full_name,
            given_name=child_in.given_name,
            gender=child_in.gender,
            level=child_in.level,
            class_name=child_in.class_name,
            date_of_birth=child_in.date_of_birth,
            nric=child_in.nric,
            transport_start_date=child_in.transport_start_date,
            transport_requirement=child_in.transport_requirement,
            block=enquiry.block,
            status="",
            school_id=enquiry.school_id,
            am_location_id=enquiry.am_location_id,
            pm_location_id=enquiry.pm_location_id,
            parent_id=parent.id,
        )
        student = student_crud.create(db, student)

    return ParentOutWithChildren.model_validate(parent)
