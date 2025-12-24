from uuid import UUID

from app.schemas.base import BaseIn, BaseOut


class BusBase(BaseIn):
    name: str
    am_plate_no: str
    am_capacity: int
    pm_plate_no: str
    pm_capacity: int
    colour: str


class BusCreate(BusBase):
    id: UUID


class BusUpdate(BusBase):
    name: str | None = None
    am_plate_no: str | None = None
    am_capacity: int | None = None
    pm_plate_no: str | None = None
    pm_capacity: int | None = None
    colour: str | None = None


class BusOut(BusBase, BaseOut):
    pass
