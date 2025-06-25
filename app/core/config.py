from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    MINIO_PRIVATE_ENDPOINT: str
    MINIO_PRIVATE_PORT: int
    MINIO_PUBLIC_ENDPOINT: str
    MINIO_PUBLIC_PORT: int
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str
    MINIO_SECURE: bool

    @computed_field
    @property
    def MINIO_PRIVATE_URL(self) -> str:
        return f"{self.MINIO_PRIVATE_ENDPOINT}:{self.MINIO_PRIVATE_PORT}"

    @computed_field
    @property
    def MINIO_PUBLIC_URL(self) -> str:
        return f"{self.MINIO_PUBLIC_ENDPOINT}:{self.MINIO_PUBLIC_PORT}"

    REVERSIBLE_ENCRYPTION_KEY: str


settings = Settings()
