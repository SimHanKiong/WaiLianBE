
from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.parent import parent_crud
from app.crud.student import student_crud
from app.schemas import StudentOut
from app.schemas.student import StudentUpdate


def read_students(db: Session) -> list[StudentOut]:
    students = student_crud.read_all(db)
    return students


def update_student(
    db: Session, id: UUID, student_in: StudentUpdate
) -> StudentOut | None:
    return student_crud.update(db, id, student_in)


def delete_students(db: Session, ids: list[UUID]) -> list[StudentOut]:
    students = student_crud.delete_all(db, ids)
    parent_ids = set()
    for student in students:
        if not student.parent or len(student.parent.children) > 0:
            continue
        parent_ids.add(student.parent.id)

    parent_crud.delete_all(db, list(parent_ids))
    return students