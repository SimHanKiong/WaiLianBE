import io
import uuid

from minio import Minio
from minio.commonconfig import CopySource

from app.core.config import settings


class MinioClient:
    def __init__(self):
        self.private_client = Minio(
            settings.MINIO_PRIVATE_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME

        if not self.private_client.bucket_exists(self.bucket_name):
            self.private_client.make_bucket(self.bucket_name)

        self.public_client = Minio(
            settings.MINIO_PUBLIC_URL,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )

    def upload(self, file_data: bytes, file_name: str, folder: str = "temp") -> str:
        extension = file_name.split(".")[-1]
        id = uuid.uuid4()
        key = f"{folder}/{id}.{extension}"
        self.private_client.put_object(
            bucket_name=self.bucket_name,
            object_name=key,
            data=io.BytesIO(file_data),
            length=len(file_data),
        )
        return key

    def delete(self, key: str) -> None:
        self.private_client.remove_object(
            bucket_name=self.bucket_name,
            object_name=key,
        )

    def rename(self, old_key: str, new_folder: str) -> str:
        new_key = f"{new_folder}/{old_key.split('/')[-1]}"
        self.private_client.copy_object(
            bucket_name=self.bucket_name,
            object_name=new_key,
            source=CopySource(self.bucket_name, old_key),
        )
        self.delete(old_key)
        return new_key

    def sign_url(self, key: str) -> str:
        return self.public_client.presigned_get_object(
            bucket_name=self.bucket_name,
            object_name=key,
        )
