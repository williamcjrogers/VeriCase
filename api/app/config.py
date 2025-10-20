from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    MINIO_ENDPOINT: str = "http://minio:9000"
    MINIO_PUBLIC_ENDPOINT: str = ""
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "changeme"
    MINIO_BUCKET: str = "vericase-docs"
    DATABASE_URL: str = "postgresql+psycopg2://vericase:vericase@postgres:5432/vericase"
    OPENSEARCH_HOST: str = "opensearch"
    OPENSEARCH_PORT: int = 9200
    OPENSEARCH_INDEX: str = "documents"
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_QUEUE: str = "ocr"
    TIKA_URL: str = "http://tika:9998"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: str = ""
    JWT_SECRET: str = "change-this-secret"
    JWT_ISSUER: str = "vericase-docs"
    JWT_EXPIRE_MIN: int = 7200
settings = Settings()
