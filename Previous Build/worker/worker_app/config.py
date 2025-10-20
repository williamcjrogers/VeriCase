import os

class Settings:
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
    MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "changeme")
    MINIO_BUCKET = os.getenv("MINIO_BUCKET", "vericase-docs")

    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://vericase:vericase@postgres:5432/vericase")

    OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "opensearch")
    OPENSEARCH_PORT = int(os.getenv("OPENSEARCH_PORT", "9200"))
    OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX", "documents")

    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CELERY_QUEUE = os.getenv("CELERY_QUEUE", "ocr")

    TIKA_URL = os.getenv("TIKA_URL", "http://tika:9998")

settings = Settings()
