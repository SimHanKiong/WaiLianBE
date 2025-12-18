from app.crud.base import CRUDBase
from app.models import Parent


parent_crud = CRUDBase[Parent](model=Parent)
