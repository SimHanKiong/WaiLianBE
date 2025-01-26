from pydantic import EmailStr
from app.schemas.base import BaseOut, BaseIn


class SchoolBase(BaseIn):
    name: str
    initial: str
    arrival_time: str
    departure_time: str
    email: EmailStr | None


class SchoolCreate(SchoolBase):
    pass


class SchoolUpdate(SchoolBase):
    name: str | None = None
    initial: str | None = None
    arrival_time: str | None = None
    departure_time: str | None = None
    email: EmailStr | None = None


class SchoolOut(SchoolBase, BaseOut):
    pass
