from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.parent import parent_crud
from app.crud.student import student_crud
from app.schemas import StudentOut, StudentOutExtended, StudentUpdate


def read_students(db: Session) -> list[StudentOutExtended]:
    students = student_crud.read_all(db)
    return [StudentOutExtended.model_validate(student) for student in students]


def update_student(
    db: Session, id: UUID, student_in: StudentUpdate
) -> StudentOut | None:
    student = student_crud.update(db, id, student_in)
    if not student:
        return None
    return StudentOut.model_validate(student)


def delete_students(db: Session, ids: list[UUID]) -> list[StudentOut]:
    students = student_crud.delete_all(db, ids)
    parent_ids = set()
    for student in students:
        if not student.parent or len(student.parent.children) > 0:
            continue
        parent_ids.add(student.parent.id)

    parent_crud.delete_all(db, list(parent_ids))
    return [StudentOut.model_validate(student) for student in students]
