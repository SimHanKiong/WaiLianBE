from typing import Generic, TypeVar
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from app.models import Base


ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model

    def read_all(
        self,
        db: Session,
        *args,
        skip: int = 0,
        limit: int = 1000,
        sort_by: str = "created_on",
    ) -> list[ModelType]:
        sort_col = getattr(self.model, sort_by.lstrip("-"))
        sort_order = desc(sort_col) if sort_by.startswith("-") else asc(sort_col)
        query = (
            select(self.model)
            .where(*args)
            .offset(skip)
            .limit(limit)
            .order_by(sort_order)
        )
        return db.execute(query).scalars().all()

    def read_one(self, db: Session, *args) -> ModelType | None:
        query = select(self.model).where(*args)
        return db.execute(query).scalars().first()

    def create(self, db: Session, obj_in: BaseModel | dict) -> ModelType:
        obj_data = (
            obj_in.model_dump(exclude_none=True, exclude_unset=True)
            if isinstance(obj_in, BaseModel)
            else obj_in
        )
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, id: UUID, obj_in: BaseModel | dict
    ) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        db_obj = db.execute(query).scalars().first()

        if not db_obj:
            return None

        obj_data = (
            obj_in.model_dump(exclude_unset=True)
            if isinstance(obj_in, BaseModel)
            else obj_in
        )

        for field, value in obj_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: UUID) -> ModelType | None:
        query = select(self.model).where(self.model.id == id)
        db_obj = db.execute(query).scalars().first()

        if not db_obj:
            return None

        db.delete(db_obj)
        db.commit()
        return db_obj
