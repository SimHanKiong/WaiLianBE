from app.schemas.base import BaseIn


class FileOut(BaseIn):
    key: str
    signed_url: str
