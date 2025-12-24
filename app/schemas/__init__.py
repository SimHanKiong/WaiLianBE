from app.schemas.base import BaseIn, BaseOut
from app.schemas.bus import BusBase, BusCreate, BusOut, BusUpdate
from app.schemas.email_body import (
    EnquiryOptionBody,
    EnquiryRegistrationBody,
    EnquiryRejectedBody,
    EnquirySentBody,
    EnquiryToBeConfirmedBody,
)
from app.schemas.enquiry import (
    EnquiryBase,
    EnquiryCreate,
    EnquiryOut,
    EnquiryStatus,
    EnquiryUpdate,
)
from app.schemas.file import FileOut
from app.schemas.location import (
    LocationBase,
    LocationCreate,
    LocationOut,
    LocationUpdate,
)
from app.schemas.parent import (
    ParentBase,
    ParentCreate,
    ParentOut,
    ParentOutWithChildren,
)
from app.schemas.school import SchoolBase, SchoolCreate, SchoolOut, SchoolUpdate
from app.schemas.student import (
    StudentBase,
    StudentCreate,
    StudentOut,
    StudentOutWithParent,
    StudentUpdate,
)


ParentOutWithChildren.model_rebuild()
StudentOutWithParent.model_rebuild()
