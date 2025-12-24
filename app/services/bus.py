from uuid import UUID

from sqlalchemy.orm import Session

from app.crud.bus import bus_crud
from app.schemas.bus import BusCreate, BusOut, BusUpdate


def read_buses(db: Session) -> list[BusOut]:
    buses = bus_crud.read_all(db)
    return [BusOut.model_validate(bus) for bus in buses]


def create_bus(db: Session, bus_in: BusCreate) -> BusOut:
    bus = bus_crud.create(db, bus_in)
    return BusOut.model_validate(bus)


def update_bus(db: Session, id: UUID, bus_in: BusUpdate) -> BusOut | None:
    bus = bus_crud.update(db, id, bus_in)
    return BusOut.model_validate(bus)


def delete_buses(db: Session, ids: list[UUID]) -> list[BusOut]:
    buses = bus_crud.delete_all(db, ids)
    return [BusOut.model_validate(bus) for bus in buses]
