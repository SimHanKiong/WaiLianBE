from uuid import UUID

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.core.exception import MissingRecordException
from app.schemas import StudentOut, StudentOutExtended, StudentUpdate
from app.services import student_service


router = APIRouter()


@router.get("/", response_model=list[StudentOutExtended])
def read_students(db: SessionDep):
    students = student_service.read_students(db)
    return students


@router.patch("/{id:uuid}", response_model=StudentOut)
def update_student(db: SessionDep, id: UUID, student_in: StudentUpdate):
    student = student_service.update_student(db, id, student_in)
    if not student:
        raise MissingRecordException("Student")
    return student


@router.delete("/", response_model=list[StudentOut])
def delete_students(db: SessionDep, ids: list[UUID]):
    students = student_service.delete_students(db, ids)
    return students
