from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # MinIO/S3
    MINIO_ENDPOINT: str = "http://minio:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "changeme"
    MINIO_BUCKET: str = "vericase-docs"

    # DB
    DATABASE_URL: str = "postgresql+psycopg2://vericase:vericase@postgres:5432/vericase"

    # OpenSearch
    OPENSEARCH_HOST: str = "opensearch"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_INDEX: str = "documents"

    # Redis/Celery
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_QUEUE: str = "ocr"

    # Tika
    TIKA_URL: str = "http://tika:9998"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # CORS
    CORS_ORIGINS: str = ""

settings = Settings()
