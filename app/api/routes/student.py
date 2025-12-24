from uuid import UUID

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.core.exception import MissingRecordException
from app.schemas import StudentOutWithParent, StudentUpdate
from app.services import student as student_service


router = APIRouter()


@router.get("/", response_model=list[StudentOutWithParent])
def read_students(db: SessionDep):
    students = student_service.read_students(db)
    return students


@router.patch("/{id:uuid}", response_model=StudentOutWithParent)
def update_student(db: SessionDep, id: UUID, student_in: StudentUpdate):
    student = student_service.update_student(db, id, student_in)
    if not student:
        raise MissingRecordException("Student")
    return student


@router.delete("/", response_model=list[StudentOutWithParent])
def delete_students(db: SessionDep, ids: list[UUID]):
    students = student_service.delete_students(db, ids)
    return students
