from fastapi import APIRouter, UploadFile

from app.core.minio import MinioClient
from app.schemas import FileOut


router = APIRouter()


@router.post("/upload", response_model=FileOut)
async def upload_temp_file(file: UploadFile):
    file_data = await file.read()
    file_client = MinioClient()
    key = file_client.upload(file_data, file.filename)
    signed_url = file_client.sign_url(key)
    return {"key": key, "signed_url": signed_url}
