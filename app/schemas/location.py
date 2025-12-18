import datetime

from app.models.route import RouteType
from app.schemas.base import BaseIn, BaseOut


class LocationBase(BaseIn):
    address: str
    time: str
    type: RouteType


class LocationCreate(LocationBase):
    pass


class LocationUpdate(LocationBase):
    address: str | None = None
    time: str | None = None
    type: RouteType | None = None
    time_reached: datetime.time | None = None
    position: float | None = None


class LocationOut(LocationBase, BaseOut):
    time_reached: datetime.time | None
    position: float | None
