from uuid import UUID
from pydantic import EmailStr
from app.schemas.base import BaseOut, BaseIn
from app.core.security import decrypt_reversible


class SchoolBase(BaseIn):
    name: str
    initial: str
    arrival_time: str
    departure_time: str
    email: EmailStr | None
    password: str
    is_final_year: bool
    email_attachment_key: str | None


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
    email_attachment_key: str | None = None


class SchoolOut(SchoolBase, BaseOut):
    email_attachment_signed_url: str | None = None

    def model_post_init(self, _) -> None:
        if self.password:
            self.password = decrypt_reversible(self.password)
