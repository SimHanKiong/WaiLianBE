from app.models.enquiry import Enquiry
from app.crud.base import CRUDBase


enquiry_crud = CRUDBase[Enquiry](model=Enquiry)
