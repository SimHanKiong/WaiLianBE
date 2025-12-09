from app.crud.base import CRUDBase
from app.models.school import School


school_crud = CRUDBase[School](model=School)
