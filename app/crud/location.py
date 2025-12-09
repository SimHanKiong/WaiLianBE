from app.crud.base import CRUDBase
from app.models.location import Location

location_crud = CRUDBase(model=Location)
