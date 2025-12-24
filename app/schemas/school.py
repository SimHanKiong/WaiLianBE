from uuid import UUID

from pydantic import EmailStr

from app.core.security import decrypt_reversible
from app.schemas.base import BaseIn, BaseOut


class SchoolBase(BaseIn):
    name: str
    initial: str
    arrival_time: str
    departure_time: str
    email: EmailStr | None
    password: str
    is_final_year: bool
    is_favourite: bool
    price_list_key: str | None
    rules_key: str | None


class SchoolCreate(SchoolBase):
    id: UUID


class SchoolUpdate(SchoolBase):
    name: str | None = None
    initial: str | None = None
    arrival_time: str | None = None
    departure_time: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_final_year: bool | None = None
    is_favourite: bool | None = None
    price_list_key: str | None = None
    rules_key: str | None = None


class SchoolOut(SchoolBase, BaseOut):
    rules_signed_url: str | None = None
    price_list_signed_url: str | None = None

    def model_post_init(self, _) -> None:
        if self.password:
            self.password = decrypt_reversible(self.password)
