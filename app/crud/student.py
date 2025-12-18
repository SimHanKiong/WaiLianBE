from app.crud.base import CRUDBase
from app.models import Student


student_crud = CRUDBase[Student](model=Student)
