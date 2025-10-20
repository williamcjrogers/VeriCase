import boto3
from botocore.client import Config
from .config import settings

_s3 = None

def s3():
    global _s3
    if _s3 is None:
        _s3 = boto3.client(
            "s3",
            endpoint_url=settings.MINIO_ENDPOINT,
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )
    return _s3

def ensure_bucket():
    client = s3()
    buckets = [b["Name"] for b in client.list_buckets().get("Buckets", [])]
    if settings.MINIO_BUCKET not in buckets:
        client.create_bucket(Bucket=settings.MINIO_BUCKET)

def put_object(key: str, data: bytes, content_type: str):
    s3().put_object(Bucket=settings.MINIO_BUCKET, Key=key, Body=data, ContentType=content_type)

def get_object(key: str) -> bytes:
    obj = s3().get_object(Bucket=settings.MINIO_BUCKET, Key=key)
    return obj["Body"].read()
