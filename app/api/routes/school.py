from uuid import UUID
from fastapi import APIRouter, HTTPException, status

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

    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="School not found"
        )

    return school


@router.post("/", response_model=SchoolOut)
def create_school(db: SessionDep, school_in: SchoolCreate):
    school = school_crud.create(db, school_in)
    return school


@router.patch("/{id:uuid}", response_model=SchoolOut)
def update_school(db: SessionDep, id: UUID, school_in: SchoolUpdate):
    school = school_crud.update(db, id, school_in)

    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="School not found"
        )

    return school


@router.delete("/{id:uuid}", response_model=SchoolOut)
def delete_school(db: SessionDep, id: UUID):
    school = school_crud.delete(db, id)

    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="School not found"
        )

    return school
