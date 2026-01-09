from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import engine
from app.core.minio import MinioClient


def get_db() -> Generator[Session, None, None]:
    with Session(engine, expire_on_commit=False) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise


def get_minio() -> MinioClient:
    return MinioClient()


SessionDep = Annotated[Session, Depends(get_db)]
MinioDep = Annotated[MinioClient, Depends(get_minio)]
