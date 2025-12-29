from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query

from app.api.deps import SessionDep
from app.core.exception import MissingRecordException
from app.schemas import (
    LocationCreate,
    LocationOut,
    LocationOutExtended,
    LocationType,
    LocationUpdate,
)
from app.services import location_service


router = APIRouter()


@router.get("/", response_model=list[LocationOutExtended])
def read_locations(
    db: SessionDep,
    type: LocationType | None = None,
    bus_id: UUID | None = None,
    sort_by: Annotated[list[str], Query()] = ["created_on"],
):
    locations = location_service.read_locations(db, type, bus_id, sort_by)
    return locations


@router.post("/", response_model=LocationOut)
def create_location(db: SessionDep, location_in: LocationCreate):
    location = location_service.create_location(db, location_in)
    return location


@router.patch("/{id:uuid}", response_model=LocationOut)
def update_location(db: SessionDep, id: UUID, location_in: LocationUpdate):
    location = location_service.update_location(db, id, location_in)
    if not location:
        raise MissingRecordException("Location")
    return location


@router.delete("/{id:uuid}", response_model=LocationOut)
def delete_location(db: SessionDep, id: UUID):
    location = location_service.delete_location(db, id)
    if not location:
        raise MissingRecordException("Location")
    return location


@router.delete("/", response_model=list[LocationOut])
def delete_locations(db: SessionDep, ids: list[UUID]):
    locations = location_service.delete_locations(db, ids)
    return locations
