from uuid import UUID
from fastapi import APIRouter, HTTPException, status

from app.models.route import RouteType
from app.schemas.location import LocationCreate, LocationOut, LocationUpdate
from app.crud.location import location_crud
from app.api.deps import SessionDep


router = APIRouter()


@router.get("/", response_model=list[LocationOut])
def read_locations(db: SessionDep, type: RouteType | None = None):
    filters = []

    if type:
        filters.append(location_crud.model.type == type)

    locations = location_crud.read_all(db, *filters)
    return locations


@router.get("/{id:uuid}", response_model=LocationOut)
def read_location(db: SessionDep, id: UUID):
    location = location_crud.read_one(db, location_crud.model.id == id)

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )

    return location


@router.post("/", response_model=LocationOut)
def create_location(db: SessionDep, location_in: LocationCreate):
    location = location_crud.create(db, location_in)
    return location


@router.patch("/{id:uuid}", response_model=LocationOut)
def update_location(db: SessionDep, id: UUID, location_in: LocationUpdate):
    location = location_crud.update(db, id, location_in)

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )

    return location


@router.delete("{id:uuid}", response_model=LocationOut)
def delete_location(db: SessionDep, id: UUID):
    location = location_crud.delete(db, id)

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Location not found"
        )

    return location