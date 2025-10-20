# VeriCase Docs — OCR + Search Service (Starter)

A production-lean starter you can run **on your machine today** and later lift to a server or cloud VM **unchanged**.

**What you get**
- 🚀 Fast full‑text search (OpenSearch)
- 🧠 Automatic OCR for scans (Tesseract via OCRmyPDF; plug‑in ABBYY later)
- 🗂️ S3‑compatible storage (MinIO) for your files
- 🧰 REST API (FastAPI) + minimal web UI
- 🧵 Asynchronous processing (Celery + Redis)
- 🧪 Tika server for rich text extraction (Word, PPT, etc.) with OCR fallback

**Run locally (Docker Desktop required)**

```bash
cp .env.example .env
docker compose up -d
# Open API docs:
# http://localhost:8000/docs
# Minimal UI:
# http://localhost:8000/ui
```

**Workflow**
1. Upload a document to `/documents` (UI or API).
2. File is stored in MinIO and a background OCR job starts.
3. Text is extracted via Tika; if empty, OCR kicks in.
4. Extracted text + metadata are indexed in OpenSearch.
5. Use `/search?q=your+terms` or the UI to find content instantly.

**Scale later**
- Move `opensearch` and `worker` to a small VPS or managed cluster.
- Keep the same compose file; just change endpoints in `.env`.

See `./api/app/config.py` and `./worker/worker_app/config.py` for environment variables.
