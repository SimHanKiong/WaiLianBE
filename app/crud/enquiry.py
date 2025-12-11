from app.crud.base import CRUDBase
from app.models.enquiry import Enquiry


enquiry_crud = CRUDBase[Enquiry](model=Enquiry)
