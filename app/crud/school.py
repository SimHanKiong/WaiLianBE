from uuid import UUID
from sqlalchemy.orm import Session


from app.core.minio import MinioClient
from app.crud.base import CRUDBase
from app.models.school import School
from app.schemas.school import SchoolCreate, SchoolUpdate
from app.core.security import encrypt_reversible


class CRUDSchool(CRUDBase[School]):
    def create(self, db: Session, school_in: SchoolCreate) -> School:
        school_in.password = encrypt_reversible(school_in.password)
        if school_in.email_attachment_key:
            file_client = MinioClient()
            new_key = file_client.rename(
                school_in.email_attachment_key, "school_email_attachments"
            )
            school_in.email_attachment_key = new_key
        return super().create(db, school_in)

    def update(self, db: Session, id: UUID, school_in: SchoolUpdate) -> School:
        if school_in.password:
            school_in.password = encrypt_reversible(school_in.password)

        if school_in.email_attachment_key:
            school = super().read_one(db, self.model.id == id)
            if not school:
                return None

            file_client = MinioClient()
            new_key = file_client.rename(
                school_in.email_attachment_key, "school_email_attachments"
            )
            school_in.email_attachment_key = new_key

            if school.email_attachment_key and school.email_attachment_key != new_key:
                old_key = school.email_attachment_key
                file_client.delete(old_key)

        return super().update(db, id, school_in)

    def delete(self, db: Session, id: UUID) -> School:
        school = super().read_one(db, self.model.id == id)
        if school and school.email_attachment_key:
            file_client = MinioClient()
            file_client.delete(school.email_attachment_key)
        return super().delete(db, id)


school_crud = CRUDSchool(model=School)
