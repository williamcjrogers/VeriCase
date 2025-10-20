# VeriCase Docs — RAPID+ (Multi-user, Direct Uploads, Previews, SDKs)

**Goals:** ultra-fast multi-user uploads & search now, with Egnyte-like building blocks (folders, sharing, versioning) and SDKs for easy integration.

**Services (Docker)**
- OpenSearch (full-text search)
- MinIO (S3-compatible object storage) — **versioning enabled + CORS**
- PostgreSQL (metadata)
- Redis + Celery (async OCR/indexing)
- Apache Tika Server (rich text extraction for Office/PDF)
- OCR worker (OCRmyPDF/Tesseract; ABBYY drop-in later)
- FastAPI (REST) + minimal UI (upload/search + PDF.js preview)

**Run**
```bash
cp .env.example .env
# Note: this compose maps to non-default ports to avoid conflicts.
docker compose up -d
# UI:   http://localhost:8010/ui
# API:  http://localhost:8010/docs
# S3:   http://localhost:9002 (MinIO API)
# Console: http://localhost:9003 (MinIO Console)
```

**Auth**
- `POST /auth/signup` → JWT
- `POST /auth/login`  → JWT
Paste token into the UI once; browser keeps it in localStorage.

**Fast Uploads**
- `POST /uploads/presign` → pre-signed PUT (browser uploads **directly to storage**)
- `POST /uploads/complete` → create doc record, enqueue OCR, index text

**Egnyte-like basics included**
- 📁 Folders/paths (`path` prefix like `projects/acme/...`)
- 🔗 Expiring share links (`POST /shares`, open `/ui/public-viewer.html?token=...`)
- 🕘 Bucket **versioning** enabled
- 🧾 **PDF.js** previews (inline viewer)

**SDKs**
- 🧩 Python: `sdk/` (already included in earlier build)
- 🟦 TypeScript: `sdk-ts/` (this repo) for browser/Node usage

