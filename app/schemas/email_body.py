from pydantic import BaseModel


class EnquirySentBody(BaseModel):
    home_address: str
    pickup_address: str
    pickup_time: str
    arrival_time: str
    dropoff_address: str
    dropoff_time: str
    departure_time: str
    fare: int


class EnquiryToBeConfirmedBody(BaseModel):
    home_address: str


class EnquiryRejectedBody(BaseModel):
    home_address: str


class EnquiryOptionBody(BaseModel):
    home_address: str
    pickup_address: str
    pickup_time: str
    arrival_time: str
    dropoff_address: str
    dropoff_time: str
    departure_time: str
    fare: int
