import io
import os
import tempfile
from datetime import datetime

from celery import Celery
import boto3
from botocore.client import Config
from sqlalchemy import create_engine, text
from opensearchpy import OpenSearch, RequestsHttpConnection
import requests
import subprocess
import pytesseract
from PIL import Image

from .config import settings

celery_app = Celery("vericase-docs", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

# S3 client (MinIO)
s3 = boto3.client(
    "s3",
    endpoint_url=settings.MINIO_ENDPOINT,
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

# DB
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# OpenSearch
os_client = OpenSearch(
    hosts=[{"host": settings.OPENSEARCH_HOST, "port": settings.OPENSEARCH_PORT}],
    http_compress=True,
    use_ssl=False,
    verify_certs=False,
    connection_class=RequestsHttpConnection,
)

def _update_status(doc_id: str, status: str, excerpt: str | None = None):
    with engine.begin() as conn:
        if excerpt is not None:
            conn.execute(text("UPDATE documents SET status=:s, text_excerpt=:e WHERE id::text=:i"), {"s": status, "e": excerpt, "i": doc_id})
        else:
            conn.execute(text("UPDATE documents SET status=:s WHERE id::text=:i"), {"s": status, "i": doc_id})

def _fetch_doc(doc_id: str):
    with engine.begin() as conn:
        row = conn.execute(text("SELECT id::text, filename, content_type, bucket, s3_key, created_at, metadata FROM documents WHERE id::text=:i"),
                           {"i": doc_id}).mappings().first()
        return dict(row) if row else None

def _index_document(doc_id: str, filename: str, created_at, content_type: str, metadata: dict, text: str):
    body = {
        "id": doc_id,
        "filename": filename,
        "title": None,
        "content_type": content_type,
        "uploaded_at": created_at,
        "metadata": metadata or {},
        "text": text
    }
    os_client.index(index=settings.OPENSEARCH_INDEX, id=doc_id, body=body, refresh=True)

def _tika_extract(file_bytes: bytes, content_type: str) -> str:
    try:
        headers = {"Accept": "text/plain"}
        # Tika Server supports auto-detection with /tika endpoint via PUT
        r = requests.put(f"{settings.TIKA_URL}/tika", data=file_bytes, headers=headers, timeout=60)
        if r.status_code == 200 and r.text:
            return r.text
    except Exception as e:
        pass
    return ""

def _ocr_pdf_sidecar(in_path: str) -> str:
    # Use ocrmypdf to produce a sidecar text file
    sidecar = in_path + ".txt"
    try:
        subprocess.run(["ocrmypdf", "--sidecar", sidecar, "--force-ocr", in_path, in_path + ".ocr.pdf"],
                       check=True, capture_output=True)
        with open(sidecar, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except subprocess.CalledProcessError as e:
        return ""
    finally:
        try:
            os.remove(sidecar)
        except Exception:
            pass

def _ocr_image_bytes(file_bytes: bytes) -> str:
    try:
        with Image.open(io.BytesIO(file_bytes)) as im:
            return pytesseract.image_to_string(im)
    except Exception:
        return ""

@celery_app.task(name="worker_app.worker.ocr_and_index", queue=settings.CELERY_QUEUE)
def ocr_and_index(doc_id: str):
    doc = _fetch_doc(doc_id)
    if not doc:
        return

    _update_status(doc_id, "PROCESSING", None)

    # download from S3
    obj = s3.get_object(Bucket=doc["bucket"], Key=doc["s3_key"])
    file_bytes = obj["Body"].read()

    text_content = ""

    # Step 1: Try Tika text extraction (handles Word, PPT, text PDFs, etc.)
    text_content = _tika_extract(file_bytes, doc.get("content_type") or "application/octet-stream")

    # Step 2: If nothing, OCR fallback
    if not text_content or len(text_content.strip()) < 50:
        filename = (doc["filename"] or "").lower()
        if filename.endswith(".pdf"):
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(file_bytes)
                tmp.flush()
                text_content = _ocr_pdf_sidecar(tmp.name) or ""
                try:
                    os.remove(tmp.name + ".ocr.pdf")
                except Exception:
                    pass
                os.remove(tmp.name)
        else:
            # Try image OCR
            text_content = _ocr_image_bytes(file_bytes) or ""

    # Index and update DB
    excerpt = (text_content.strip()[:1000]) if text_content else ""
    _index_document(doc_id, doc["filename"], doc["created_at"], doc.get("content_type") or "application/octet-stream", doc.get("metadata"), text_content or "")
    _update_status(doc_id, "READY", excerpt)
    return {"id": doc_id, "chars": len(text_content)}
