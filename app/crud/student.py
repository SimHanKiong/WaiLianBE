from app.crud.base import CRUDBase
from app.models.student import Student


student_crud = CRUDBase[Student](model=Student)
