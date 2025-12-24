from app.crud.base import CRUDBase
from app.models import Bus


bus_crud = CRUDBase[Bus](model=Bus)
