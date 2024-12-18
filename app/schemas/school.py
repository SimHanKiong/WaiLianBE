from uuid import UUID
from app.schemas.base import BaseOut, BaseIn


class SchoolBase(BaseIn):
    name: str
    initial: str
    arrival_time: str
    departure_time: str


class SchoolCreate(SchoolBase):
    id: UUID | None = None


class SchoolUpdate(SchoolBase):
    name: str | None = None
    initial: str | None = None
    arrival_time: str | None = None
    departure_time: str | None = None


class SchoolOut(SchoolBase, BaseOut):
    pass
