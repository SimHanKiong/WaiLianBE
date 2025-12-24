from uuid import UUID

from sqlalchemy.orm import Session

from app.core.minio import MinioClient
from app.core.security import encrypt_reversible
from app.crud.school import school_crud
from app.models import School
from app.schemas import SchoolCreate, SchoolOut, SchoolUpdate


def read_schools(db: Session, minio: MinioClient) -> list[SchoolOut]:
    schools = school_crud.read_all(db)
    return [sign_keys(school, minio) for school in schools]


def read_school(db: Session, minio: MinioClient, id: UUID) -> SchoolOut | None:
    school = school_crud.read_one(db, school_crud.model.id == id)
    if not school:
        return None
    return sign_keys(school, minio)


def create_school(
    db: Session, minio: MinioClient, school_in: SchoolCreate
) -> SchoolOut:
    if school_in.password:
        school_in.password = encrypt_reversible(school_in.password)

    if school_in.price_list_key:
        new_key = minio.rename(school_in.price_list_key, "school_price_lists")
        school_in.price_list_key = new_key

    if school_in.rules_key:
        new_key = minio.rename(school_in.rules_key, "school_rules")
        school_in.rules_key = new_key

    school = school_crud.create(db, school_in)
    return sign_keys(school, minio)


def update_school(
    db: Session, minio: MinioClient, id: UUID, school_in: SchoolUpdate
) -> SchoolOut | None:
    school = school_crud.read_one(db, school_crud.model.id == id)
    if not school:
        return None

    if school_in.password:
        school_in.password = encrypt_reversible(school_in.password)

    if school_in.price_list_key:
        new_key = minio.rename(school_in.price_list_key, "school_price_lists")
        school_in.price_list_key = new_key

        if school.price_list_key and school.price_list_key != new_key:
            minio.delete(school.price_list_key)

    if school_in.rules_key:
        new_key = minio.rename(school_in.rules_key, "school_rules")
        school_in.rules_key = new_key

        if school.rules_key and school.rules_key != new_key:
            minio.delete(school.rules_key)

    school = school_crud.update(db, id, school_in)
    return sign_keys(school, minio)


def delete_schools(db: Session, minio: MinioClient, ids: list[UUID]) -> list[SchoolOut]:
    schools = school_crud.delete_all(db, ids)
    for school in schools:
        if school.price_list_key:
            minio.delete(school.price_list_key)
        if school.rules_key:
            minio.delete(school.rules_key)
    return [sign_keys(school, minio) for school in schools]


def sign_keys(school: School, minio: MinioClient) -> SchoolOut:
    school_out = SchoolOut.model_validate(school)
    if school.price_list_key:
        signed_url = minio.sign_url(school.price_list_key)
        school_out.price_list_signed_url = signed_url
    if school.rules_key:
        signed_url = minio.sign_url(school.rules_key)
        school_out.rules_signed_url = signed_url
    return school_out
