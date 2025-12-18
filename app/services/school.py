import re

from uuid import UUID

from sqlalchemy.orm import Session

from app.core.minio import MinioClient
from app.core.security import encrypt_reversible
from app.crud.school import school_crud
from app.models import School
from app.schemas import SchoolCreate, SchoolOut, SchoolUpdate


def read_schools(db: Session, minio: MinioClient) -> list[SchoolOut]:
    schools = school_crud.read_all(db)
    return [sign_email_attachment(school, minio) for school in schools]


def read_school(db: Session, minio: MinioClient, id: UUID) -> School | None:
    school = school_crud.read_one(db, school_crud.model.id == id)
    if not school:
        return None
    return sign_email_attachment(school, minio)


def create_school(
    db: Session, minio: MinioClient, school_in: SchoolCreate
) -> SchoolOut:
    if school_in.password:
        school_in.password = encrypt_reversible(school_in.password)

    if school_in.email_attachment_key:
        new_key = minio.rename(
            school_in.email_attachment_key, "school_email_attachments"
        )
        school_in.email_attachment_key = new_key

    school = school_crud.create(db, school_in)
    return sign_email_attachment(school, minio)


def update_school(
    db: Session, minio: MinioClient, id: UUID, school_in: SchoolUpdate
) -> SchoolOut | None:
    school = school_crud.read_one(db, school_crud.model.id == id)
    if not school:
        return None

    if school_in.password:
        school_in.password = encrypt_reversible(school_in.password)

    if school_in.email_attachment_key:
        new_key = minio.rename(
            school_in.email_attachment_key, "school_email_attachments"
        )
        school_in.email_attachment_key = new_key

        if school.email_attachment_key and school.email_attachment_key != new_key:
            minio.delete(school.email_attachment_key)

    school = school_crud.update(db, id, school_in)
    return sign_email_attachment(school, minio)


def delete_schools(db: Session, minio: MinioClient, ids: list[UUID]) -> list[SchoolOut]:
    schools = school_crud.delete_all(db, ids)
    for school in schools:
        if school.email_attachment_key:
            minio.delete(school.email_attachment_key)
    return [sign_email_attachment(school, minio) for school in schools]


def sign_email_attachment(school: School, minio: MinioClient) -> SchoolOut:
    if not school.email_attachment_key:
        return SchoolOut.model_validate(school)
    signed_url = minio.sign_url(school.email_attachment_key)
    school_out = SchoolOut.model_validate(school)
    school_out.email_attachment_signed_url = signed_url
    return school_out
