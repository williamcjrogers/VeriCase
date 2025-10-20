import logging
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
from uuid import uuid4
from fastapi import FastAPI, Depends, HTTPException, Query, Body, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session, joinedload
from .config import settings
from .db import Base, engine
from .models import Document, DocStatus, User, ShareLink
from .storage import ensure_bucket, presign_put, presign_get, multipart_start, presign_part, multipart_complete, s3, get_object, put_object, delete_object
from .search import ensure_index, search as os_search, delete_document as os_delete
from .tasks import celery_app
from .security import get_db, current_user, hash_password, verify_password, sign_token
from .watermark import build_watermarked_pdf, normalize_watermark_text
from pydantic import BaseModel

logger = logging.getLogger(__name__)


def _parse_uuid(value: str) -> uuid.UUID:
    try:
        return uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        raise HTTPException(400, "invalid document id")


class DocumentSummary(BaseModel):
    id: str
    filename: str
    path: Optional[str] = None
    status: str
    size: int
    content_type: Optional[str] = None
    title: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class DocumentListResponse(BaseModel):
    total: int
    items: List[DocumentSummary]


class PathListResponse(BaseModel):
    paths: List[str]
app = FastAPI(title="VeriCase Docs API", version="0.3.0")
origins=[o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
if origins:
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
_here = Path(__file__).resolve()
_base_dir = _here.parent.parent  # /code or repo/api
_ui_candidates = [
    _base_dir / "ui",
    _base_dir.parent / "ui",
]
UI_DIR = next((c for c in _ui_candidates if c.exists()), None)
if UI_DIR:
    app.mount("/ui", StaticFiles(directory=str(UI_DIR), html=True), name="ui")
else:
    logger.warning("UI directory not found in candidates %s; /ui mount disabled", _ui_candidates)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/ui/")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine); ensure_bucket(); ensure_index()
# Auth
@app.post("/auth/signup")
def signup(payload: dict = Body(...), db: Session = Depends(get_db)):
    email=(payload.get("email") or "").strip().lower(); password=payload.get("password") or ""
    if not email or not password: raise HTTPException(400,"email and password required")
    from .models import User
    if db.query(User).filter(User.email==email).first(): raise HTTPException(409,"email already registered")
    user=User(email=email, password_hash=hash_password(password)); db.add(user); db.commit()
    token=sign_token(str(user.id), user.email); return {"token": token, "user":{"id":str(user.id),"email":user.email}}
@app.post("/auth/login")
def login(payload: dict = Body(...), db: Session = Depends(get_db)):
    email=(payload.get("email") or "").strip().lower(); password=payload.get("password") or ""
    user=db.query(User).filter(User.email==email).first()
    if not user or not verify_password(password, user.password_hash): raise HTTPException(401,"invalid credentials")
    token=sign_token(str(user.id), user.email); return {"token": token, "user":{"id":str(user.id),"email":user.email}}
# Uploads (presign and complete)
@app.post("/uploads/presign")
def presign_upload(body: dict = Body(...), user: User = Depends(current_user)):
    filename=body.get("filename"); ct=body.get("content_type") or "application/octet-stream"
    path=(body.get("path") or "").strip().strip("/")
    key=f"{path + '/' if path else ''}{uuid.uuid4()}/{filename}"
    url=presign_put(key, ct); return {"key":key, "url":url}
@app.post("/uploads/complete")
def complete_upload(body: dict = Body(...), db: Session = Depends(get_db), user: User = Depends(current_user)):
    from .models import Document, DocStatus
    key=body.get("key"); filename=body.get("filename") or "file"; ct=body.get("content_type") or "application/octet-stream"
    size=int(body.get("size") or 0); title=body.get("title"); path=body.get("path")
    doc=Document(filename=filename, path=path, content_type=ct, size=size, bucket=settings.MINIO_BUCKET, s3_key=key, title=title, status=DocStatus.NEW, owner_user_id=user.id)
    db.add(doc); db.commit(); celery_app.send_task("worker_app.worker.ocr_and_index", args=[str(doc.id)])
    return {"id": str(doc.id), "status":"QUEUED"}
@app.post("/uploads/multipart/start")
def multipart_start_ep(body: dict = Body(...), user: User = Depends(current_user)):
    filename=body.get("filename"); ct=body.get("content_type") or "application/octet-stream"
    path=(body.get("path") or "").strip().strip("/"); key=f"{path + '/' if path else ''}{uuid.uuid4()}/{filename}"
    upload_id=multipart_start(key, ct); return {"key":key, "uploadId": upload_id}
@app.get("/uploads/multipart/part")
def multipart_part_url(key: str, uploadId: str, partNumber: int, user: User = Depends(current_user)):
    return {"url": presign_part(key, uploadId, partNumber)}
@app.post("/uploads/multipart/complete")
def multipart_complete_ep(body: dict = Body(...), db: Session = Depends(get_db), user: User = Depends(current_user)):
    key=body["key"]; upload_id=body["uploadId"]; parts=body["parts"]; multipart_complete(key, upload_id, parts)
    filename=body.get("filename") or "file"; ct=body.get("content_type") or "application/octet-stream"
    size=int(body.get("size") or 0); title=body.get("title"); path=body.get("path")
    doc=Document(filename=filename, path=path, content_type=ct, size=size, bucket=settings.MINIO_BUCKET, s3_key=key, title=title, status=DocStatus.NEW, owner_user_id=user.id)
    db.add(doc); db.commit(); celery_app.send_task("worker_app.worker.ocr_and_index", args=[str(doc.id)])
    return {"id": str(doc.id), "status":"QUEUED"}


@app.get("/documents", response_model=DocumentListResponse)
def list_documents(
    path_prefix: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    query = db.query(Document).filter(Document.owner_user_id == user.id)
    if path_prefix:
        safe_path = path_prefix.strip().strip("/")
        if safe_path:
            like_pattern = f"{safe_path}%"
            query = query.filter(Document.path.like(like_pattern))
    if status:
        try:
            status_enum = DocStatus(status.upper())
        except ValueError:
            raise HTTPException(400, "invalid status value")
        query = query.filter(Document.status == status_enum)
    total = query.count()
    docs = query.order_by(Document.created_at.desc()).offset(offset).limit(limit).all()
    items = [
        DocumentSummary(
            id=str(doc.id),
            filename=doc.filename,
            path=doc.path,
            status=doc.status.value if doc.status else DocStatus.NEW.value,
            size=doc.size or 0,
            content_type=doc.content_type,
            title=doc.title,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
        )
        for doc in docs
    ]
    return DocumentListResponse(total=total, items=items)


@app.get("/documents/paths", response_model=PathListResponse)
def list_paths(
    db: Session = Depends(get_db),
    user: User = Depends(current_user),
):
    paths = (
        db.query(Document.path)
        .filter(Document.owner_user_id == user.id, Document.path.isnot(None))
        .distinct().all()
    )
    path_values = sorted(
        p[0]
        for p in paths
        if p[0]
    )
    return PathListResponse(paths=path_values)

# Documents
@app.get("/documents/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    doc=db.get(Document, _parse_uuid(doc_id))
    if not doc:
        raise HTTPException(404,"not found")
    return {"id":str(doc.id),"filename":doc.filename,"path":doc.path,"status":doc.status.value,
            "content_type":doc.content_type,"size":doc.size,"bucket":doc.bucket,"s3_key":doc.s3_key,
            "title":doc.title,"metadata":doc.meta,"text_excerpt":(doc.text_excerpt or "")[:1000],
            "created_at":doc.created_at,"updated_at":doc.updated_at}
@app.get("/documents/{doc_id}/signed_url")
def get_signed_url(doc_id: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    doc=db.get(Document, _parse_uuid(doc_id))
    if not doc:
        raise HTTPException(404,"not found")
    return {"url": presign_get(doc.s3_key, 300), "filename": doc.filename, "content_type": doc.content_type}


@app.delete("/documents/{doc_id}", status_code=204)
def delete_document_endpoint(doc_id: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    doc = db.get(Document, _parse_uuid(doc_id))
    if not doc or doc.owner_user_id != user.id:
        raise HTTPException(404, "not found")
    try:
        delete_object(doc.s3_key)
    except Exception:
        logger.exception("Failed to delete object %s from storage", doc.s3_key)
    try:
        os_delete(str(doc.id))
    except Exception:
        logger.exception("Failed to delete document %s from search index", doc.id)
    db.delete(doc)
    db.commit()
    return Response(status_code=204)
# Search
@app.get("/search")
def search(q: str = Query(..., min_length=1), path_prefix: Optional[str] = None, user: User = Depends(current_user)):
    res=os_search(q, size=25, path_prefix=path_prefix); hits=[]
    for h in res.get("hits",{}).get("hits",[]):
        src=h.get("_source",{})
        hits.append({"id":src.get("id"),"filename":src.get("filename"),"title":src.get("title"),
                     "path":src.get("path"),"content_type":src.get("content_type"),"score":h.get("_score"),
                     "snippet":" ... ".join(h.get("highlight",{}).get("text", src.get("text","")[:200:])) if h.get("highlight") else None})
    return {"count": len(hits), "hits": hits}
# Share links
@app.post("/shares")
def create_share(body: dict = Body(...), db: Session = Depends(get_db), user: User = Depends(current_user)):
    doc_id=body.get("document_id"); hours=int(body.get("hours") or 24)
    if not doc_id:
        raise HTTPException(400, "document_id required")
    doc=db.get(Document, _parse_uuid(doc_id))
    if not doc:
        raise HTTPException(404,"document not found")
    if hours < 1:
        hours = 1
    if hours > 168:
        hours = 168
    password = body.get("password")
    password_hash = None
    if password:
        password = password.strip()
        if len(password) < 4 or len(password) > 128:
            raise HTTPException(400, "password length must be between 4 and 128 characters")
        password_hash = hash_password(password)
    token=uuid.uuid4().hex; expires=datetime.utcnow() + timedelta(hours=hours)
    share=ShareLink(token=token, document_id=doc.id, created_by=user.id, expires_at=expires, password_hash=password_hash); db.add(share); db.commit()
    return {"token": token, "expires_at": expires, "requires_password": bool(password_hash)}
@app.get("/shares/{token}")
def resolve_share(token: str, password: Optional[str] = Query(default=None), watermark: Optional[str] = Query(default=None), db: Session = Depends(get_db)):
    now=datetime.utcnow()
    share=db.query(ShareLink).options(joinedload(ShareLink.document)).filter(ShareLink.token==token, ShareLink.expires_at>now).first()
    if not share: raise HTTPException(404,"invalid or expired")
    if share.password_hash:
        if not password or not verify_password(password, share.password_hash):
            raise HTTPException(401,"password required")
    document = share.document
    if not document:
        raise HTTPException(500,"document missing")
    if watermark:
        sanitized = normalize_watermark_text(watermark)
        if not sanitized:
            raise HTTPException(400,"watermark must contain printable characters")
        content_type = (document.content_type or "").lower()
        filename = (document.filename or "")
        if "pdf" not in content_type and not filename.lower().endswith(".pdf"):
            raise HTTPException(400,"watermark supported for PDFs only")
        try:
            original_bytes = get_object(document.s3_key)
            stamped = build_watermarked_pdf(original_bytes, sanitized)
            temp_key = f"shares/{token}/watermarked/{uuid4()}.pdf"
            put_object(temp_key, stamped, "application/pdf")
            url = presign_get(temp_key, 300)
            return {"url": url, "filename": filename, "content_type": "application/pdf"}
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Failed to create watermarked PDF for share %s", token)
            raise HTTPException(500,"unable to generate watermark") from exc
    url=presign_get(document.s3_key, 300)
    return {"url": url, "filename": document.filename, "content_type": document.content_type}
