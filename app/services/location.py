from uuid import UUID

from sqlalchemy.orm import Session

from app.core.minio import MinioClient
from app.core.security import encrypt_reversible
from app.crud.location import location_crud
from app.models import Location
from app.schemas import LocationCreate, LocationOut, LocationOutExtended, LocationUpdate
from app.schemas.location import LocationType


def read_locations(
    db: Session, type: LocationType | None, bus_id: UUID | None, sort_by: list[str]
) -> list[LocationOutExtended]:
    filters = []
    if type:
        filters.append(location_crud.model.type == type)
    if bus_id:
        filters.append(location_crud.model.bus_id == bus_id)
    locations = location_crud.read_all(db, *filters, sort_by=sort_by)
    return [LocationOutExtended.model_validate(location) for location in locations]


def create_location(db: Session, location_in: LocationCreate) -> LocationOut:
    location = location_crud.create(db, location_in)
    return LocationOut.model_validate(location)


def update_location(
    db: Session, id: UUID, location_in: LocationUpdate
) -> LocationOut | None:
    location = location_crud.update(db, id, location_in)
    return LocationOut.model_validate(location) if location else None


def delete_location(db: Session, id: UUID) -> LocationOut | None:
    location = location_crud.delete(db, id)
    return LocationOut.model_validate(location) if location else None


def delete_locations(db: Session, ids: list[UUID]) -> list[LocationOut]:
    locations = location_crud.delete_all(db, ids)
    return [LocationOut.model_validate(location) for location in locations]
