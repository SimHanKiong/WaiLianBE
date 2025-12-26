from uuid import UUID

from app.models.route import RouteType
from app.schemas.base import BaseIn, BaseOut
from app.schemas.bus import BusOut


class LocationBase(BaseIn):
    address: str
    time: str
    type: RouteType
    bus_id: UUID | None


class LocationCreate(LocationBase):
    bus_id: UUID | None = None


class LocationUpdate(LocationBase):
    address: str | None = None
    time: str | None = None
    type: RouteType | None = None
    bus_id: UUID | None = None


class LocationOut(LocationBase, BaseOut):
    bus: BusOut | None
