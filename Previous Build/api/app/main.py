import io
import uuid
from datetime import datetime
from typing import Optional, List

from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .config import settings
from .db import Base, engine, SessionLocal
from .models import Document, DocStatus
from .storage import ensure_bucket, put_object
from .search import ensure_index, search as os_search
from .tasks import celery_app

app = FastAPI(title="VeriCase Docs API", version="0.1.0")

# CORS
origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Static minimal UI
app.mount("/ui", StaticFiles(directory="/code/ui", html=True), name="ui")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    ensure_bucket()
    ensure_index()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    content = await file.read()
    doc_id = uuid.uuid4()
    s3_key = f"{doc_id}/{file.filename}"

    put_object(s3_key, content, file.content_type or "application/octet-stream")

    doc = Document(
        id=doc_id,
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        size=len(content),
        bucket=settings.MINIO_BUCKET,
        s3_key=s3_key,
        title=title,
        metadata=None,
        status=DocStatus.NEW,
    )
    db.add(doc)
    db.commit()

    # Enqueue OCR+indexing task
    celery_app.send_task("worker_app.worker.ocr_and_index", args=[str(doc_id)])

    return {"id": str(doc_id), "status": "QUEUED"}

@app.get("/documents/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    doc = db.get(Document, doc_id)
    if not doc:
        return JSONResponse({"error": "not found"}, status_code=404)
    return {
        "id": str(doc.id),
        "filename": doc.filename,
        "status": doc.status.value,
        "content_type": doc.content_type,
        "size": doc.size,
        "bucket": doc.bucket,
        "s3_key": doc.s3_key,
        "title": doc.title,
        "metadata": doc.metadata,
        "text_excerpt": (doc.text_excerpt or "")[:500],
        "created_at": doc.created_at,
        "updated_at": doc.updated_at,
    }

@app.get("/search")
def search(q: str):
    res = os_search(q, size=25)
    hits = []
    for h in res.get("hits", {}).get("hits", []):
        src = h.get("_source", {})
        hits.append({
            "id": src.get("id"),
            "filename": src.get("filename"),
            "title": src.get("title"),
            "score": h.get("_score"),
            "snippet": " ... ".join(h.get("highlight", {}).get("text", src.get("text","")[:200:])) if h.get("highlight") else None
        })
    return {"count": len(hits), "hits": hits}
