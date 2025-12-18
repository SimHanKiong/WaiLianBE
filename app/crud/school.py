from app.crud.base import CRUDBase
from app.models import School


school_crud = CRUDBase[School](model=School)
