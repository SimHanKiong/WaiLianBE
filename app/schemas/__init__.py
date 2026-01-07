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
    LocationOutExtended,
    LocationType,
    LocationUpdate,
)
from app.schemas.parent import (
    ParentBase,
    ParentCreate,
    ParentCreateFromEnquiry,
    ParentOut,
    ParentOutExtended,
)
from app.schemas.school import SchoolBase, SchoolCreate, SchoolOut, SchoolUpdate
from app.schemas.student import (
    StudentBase,
    StudentCreate,
    StudentCreateFromEnquiry,
    StudentOut,
    StudentOutExtended,
    StudentUpdate,
)


ParentOutExtended.model_rebuild()
StudentOutExtended.model_rebuild()
LocationOutExtended.model_rebuild()
