from uuid import UUID
from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from app.core.exception import raise_database_exception, raise_missing_exception
from app.schemas.school import SchoolCreate, SchoolOut, SchoolUpdate
from app.crud.school import school_crud
from app.api.deps import SessionDep


router = APIRouter()


@router.get("/", response_model=list[SchoolOut])
def read_schools(
    db: SessionDep,
):
    schools = school_crud.read_all(db)
    return schools


@router.get("/{id:uuid}", response_model=SchoolOut)
def read_school(db: SessionDep, id: UUID):
    school = school_crud.read_one(db, school_crud.model.id == id)
    return raise_missing_exception(school, 'School')


@router.post("/", response_model=SchoolOut)
def create_school(db: SessionDep, school_in: SchoolCreate):
    try:
        school = school_crud.create(db, school_in)
        return school
    except IntegrityError as e:
        raise_database_exception(e, "School")


@router.patch("/{id:uuid}", response_model=SchoolOut)
def update_school(db: SessionDep, id: UUID, school_in: SchoolUpdate):
    try:
        school = school_crud.update(db, id, school_in)
        return raise_missing_exception(school, 'School') 
    except IntegrityError as e:
        raise_database_exception(e, "School")


@router.delete("/{id:uuid}", response_model=SchoolOut)
def delete_school(db: SessionDep, id: UUID):
    school = school_crud.delete(db, id)
    return raise_missing_exception(school, 'School')
