from sqlalchemy.orm import Session


from app.crud.base import CRUDBase
from app.models.school import School
from app.schemas.school import SchoolCreate
from app.core.security import encrypt_reversible


class CRUDSchool(CRUDBase[School]):

    def create(self, db: Session, school_in: SchoolCreate) -> School:
        school_in.password = encrypt_reversible(school_in.password)
        return super().create(db, school_in)
    
    def update(self, db: Session, id: str, school_in: SchoolCreate) -> School:
        if school_in.password:
            school_in.password = encrypt_reversible(school_in.password)
        return super().update(db, id, school_in)
    
school_crud = CRUDSchool(model=School)
