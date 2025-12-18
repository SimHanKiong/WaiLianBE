from uuid import UUID

from fastapi import APIRouter

from app.api.deps import MinioDep, SessionDep
from app.core.exception import MissingRecordException
from app.schemas import SchoolCreate, SchoolOut, SchoolUpdate
from app.services import school as school_service


router = APIRouter()


@router.get("/", response_model=list[SchoolOut])
def read_schools(db: SessionDep, minio: MinioDep):
    schools = school_service.read_schools(db, minio)
    return schools


@router.get("/{id:uuid}", response_model=SchoolOut)
def read_school(db: SessionDep, minio: MinioDep, id: UUID):
    school = school_service.read_school(db, minio, id)
    if not school:
        raise MissingRecordException("School")
    return school


@router.post("/", response_model=SchoolOut)
def create_school(db: SessionDep, minio: MinioDep, school_in: SchoolCreate):
    school = school_service.create_school(db, minio, school_in)
    return school


@router.patch("/{id:uuid}", response_model=SchoolOut)
def update_school(db: SessionDep, minio: MinioDep, id: UUID, school_in: SchoolUpdate):
    school = school_service.update_school(db, minio, id, school_in)
    if not school:
        raise MissingRecordException("School")
    return school


@router.delete("/", response_model=list[SchoolOut])
def delete_schools(db: SessionDep, minio: MinioDep, ids: list[UUID]):
    schools = school_service.delete_schools(db, minio, ids)
    return schools
