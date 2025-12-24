from uuid import UUID

from fastapi import APIRouter

from app.api.deps import SessionDep
from app.core.exception import MissingRecordException
from app.schemas import BusCreate, BusOut, BusUpdate
from app.services import bus as bus_service


router = APIRouter()


@router.get("/", response_model=list[BusOut])
def read_buses(db: SessionDep):
    buses = bus_service.read_buses(db)
    return buses


@router.post("/", response_model=BusOut)
def create_bus(db: SessionDep, bus_in: BusCreate):
    bus = bus_service.create_bus(db, bus_in)
    return bus


@router.patch("/{id:uuid}", response_model=BusOut)
def update_bus(db: SessionDep, id: UUID, bus_in: BusUpdate):
    bus = bus_service.update_bus(db, id, bus_in)
    if not bus:
        raise MissingRecordException("Bus")
    return bus


@router.delete("/", response_model=list[BusOut])
def delete_buses(db: SessionDep, ids: list[UUID]):
    buses = bus_service.delete_buses(db, ids)
    return buses
