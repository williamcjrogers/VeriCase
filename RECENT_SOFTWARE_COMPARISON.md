# VeriCase Codebase Comparison

_Last reviewed: 2025-11-02_

This note compares the three VeriCase worktrees currently open in VS Code and highlights which capabilities exist where, plus guidance on how to consolidate the best parts.

## 1. `vericase-docs-rapid-plus-ts` (current active repo)

**Focus:** Modern document vault with AI support

- **Auth:** Email/password with JWT (FastAPI + custom security)
- **Storage:** MinIO/S3 with dual endpoint support, presigned URLs, multipart uploads
- **Search:** OpenSearch full-text index, OCR pipeline, Celery worker, Apache Tika, OCRmyPDF, pytesseract
- **Domain model:** `Document`, `Folder`, `ShareLink`, `Favorite`, `DocumentVersion`; per-user ownership, admin override, path-based folders
- **AI:** Orchestrated AI endpoints, classification tasks routed through Celery
- **UI:** Polished single-page app in `/ui` with folder tree, upload modal, share links, watermarking, favorites, versioning
- **Infrastructure:** Docker Compose stack (api, worker, postgres, redis, opensearch, tika, minio), PowerShell/Bash deploy scripts, AWS-ready configuration
- **Strengths:** Production-grade pipeline, robust storage abstraction, advanced features (watermarking, favorites, share links, AI orchestration)
- **Gaps:** No explicit "cases / issues / evidence" hierarchy; PST/MSG email parsing still pending (storage only)

## 2. `VeriCase-DESKTOP-46BMPM4/vericase-integrated`

**Focus:** Case-centric evidence tracker with OIDC integration (prototype)

- **Auth:** Azure AD / generic OIDC via JWT middleware (`auth.py`)
- **Domain model:** `Case`, `Evidence`, `Issue`, `Job` tables; issue↔evidence linking with rationale notes
- **Storage:** Simple S3 client wrapper plus job queue & archive extraction (ZIP unfolding, PST stub)
- **Processing:** Polling worker that extracts ZIP contents into child evidence records; placeholder for PST parsing
- **Search:** Per-case keyword search + TF‑IDF semantic ranking (in-process, no external search engine)
- **API surface:** `/cases`, `/evidence`, `/issues`, `/jobs`, `/export/issue`, `/embeddings/test`
- **Strengths:** Case/issue schema, job orchestration hooks, OIDC-ready security layer; PST awareness (stub)
- **Gaps:** Minimal UI (not included here), limited text extraction (no Tika/OCR), SQLite default, no advanced document features (folders, share links)

## 3. `VeriCase-DESKTOP-PE31924/VeriCase_Builder_Pack`

**Focus:** Earlier builder pack (FastAPI + Next.js) emphasising claims/chronology workflows

- **Backend:** Modular FastAPI routers for cases, evidence, search, claims, rebuttals, chronology, exports
- **Storage:** Local filesystem saves under `var/evidence`; light-weight extraction for `.txt` files only
- **Search:** OpenSearch "hybrid" search with knn vectors; embeddings generated via OpenAI/other providers (1536-dim vectors)
- **AI:** `ai/embeddings.py` wrappers; chronologies/rebuttals leveraging LLM prompts (see docs in `docs/`)
- **Frontend:** Next.js app (`vericase-starter`) with rich UI components for case workspace, timeline, claims management
- **Strengths:** Well-organized frontend, domain concepts for legal workflows (claims, chronology, rebuttal), KNN vector search scaffolding
- **Gaps:** Backend ingestion limited (no OCR, no MinIO/S3, no Celery), auth unspecified, prototype-only storage

## Recommended Consolidation Strategy

1. **Anchor on `vericase-docs-rapid-plus-ts`** for core infrastructure (storage, Celery/Tika/OCR, OpenSearch, MinIO, share links, foldering, AI orchestrator).
2. **Port domain entities from `vericase-integrated`**:
   - Introduce `Case`, `Issue`, `Evidence` tables alongside existing `Document` model, reusing SQLAlchemy migrations.
   - Reuse issue↔evidence linking logic for legal workflows; map `Document` records to `Evidence` entries when uploaded under a case path (e.g. `cases/<case-id>/...`).
   - Adapt job queue integration to Celery (replace polling worker); move ZIP/PST extraction stubs into Celery tasks.
3. **Fold in OIDC middleware** for enterprise SSO while keeping existing JWT auth as fallback (feature flag via settings).
4. **Leverage `VeriCase_Builder_Pack` UI/UX**:
   - Reuse Next.js components for claims/chronology dashboards, embedding them into the current UI (or host as separate app that calls the unified API).
   - Migrate OpenSearch KNN vector index definition so current `search` package can support semantic filtering per case.
5. **PST/MSG/EML extraction:** upgrade old stub to use real parsers (`pypff`, `extract_msg`, `mail-parser`) within the current worker. Share logic across evidence ingestion and document AI pipelines.
6. **Documentation:** consolidate guides (deployment, feature plans) under `/docs`; note SSO setup steps, case workflow, AI modules.

## Immediate Action Items

- [ ] Decide on canonical database schema (extend current Alembic migrations with case/issue tables).
- [ ] Extract reusable services (storage, indexing) into shared modules so legacy endpoints can be reimplemented using the modern stack.
- [ ] Review Next.js app to estimate effort of porting UI pieces vs. extending existing vanilla JS UI.
- [ ] Create migration plan for users/documents already stored (how to associate with new `Case` records or remain standalone).
- [ ] Prioritise PST extraction upgrade (see `PST_FILE_SUPPORT_ANALYSIS.md`).

Use this matrix as a reference while merging code so we keep the production-ready parts from the main repo and selectively bring over advanced legal workflows and SSO from the other workspaces.
