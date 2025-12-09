from uuid import UUID
from pydantic import EmailStr, computed_field
from app.schemas.base import BaseOut, BaseIn
from app.core.security import decrypt_reversible
from app.core.minio import MinioClient


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
    pass


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
    def model_post_init(self, _) -> None:
        if self.password:
            self.password = decrypt_reversible(self.password)

    @computed_field
    @property
    def email_attachment_signed_url(self) -> str | None:
        if not self.email_attachment_key:
            return None
        file_client = MinioClient()
        return file_client.sign_url(self.email_attachment_key)
