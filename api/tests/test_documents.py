import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Generator, Tuple

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app  # noqa: E402
from app.models import Base, Document, DocStatus, User  # noqa: E402
from app.security import current_user as real_current_user, get_db as real_get_db  # noqa: E402


ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=ENGINE, autocommit=False, autoflush=False)


@pytest.fixture()
def client() -> Generator[Tuple[TestClient, Session, User], None, None]:
    Base.metadata.create_all(bind=ENGINE)
    session = TestingSessionLocal()

    user = User(email="tester@example.com", password_hash="hashed")
    session.add(user)
    session.commit()
    session.refresh(user)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_current_user():
        # Return a fresh instance attached to the current override session
        with TestingSessionLocal() as db:
            return db.get(User, user.id)

    app.dependency_overrides[real_get_db] = override_get_db
    app.dependency_overrides[real_current_user] = override_current_user

    original_startup = list(app.router.on_startup)
    original_shutdown = list(app.router.on_shutdown)
    app.router.on_startup.clear()
    app.router.on_shutdown.clear()

    try:
        with TestClient(app) as test_client:
            yield test_client, session, user
    finally:
        app.router.on_startup[:] = original_startup
        app.router.on_shutdown[:] = original_shutdown
        app.dependency_overrides.clear()
        session.close()
        Base.metadata.drop_all(bind=ENGINE)


def _make_document(owner_id, path, filename, created_offset_minutes, size=1024):
    created_at = datetime.now(timezone.utc) + timedelta(minutes=created_offset_minutes)
    return Document(
        filename=filename,
        path=path,
        status=DocStatus.READY,
        size=size,
        bucket="bucket",
        s3_key=f"{path}/{filename}",
        content_type="application/pdf",
        owner_user_id=owner_id,
        created_at=created_at,
    )


def test_list_documents_filters_and_paginates(client):
    test_client, session, user = client

    docs = [
        _make_document(user.id, "projects/acme/contracts", "contract-a.pdf", 0, size=1000),
        _make_document(user.id, "projects/acme/reports", "report-b.pdf", 5, size=2000),
        _make_document(user.id, "projects/beta/notes", "notes-c.pdf", 10, size=3000),
    ]
    other_user = User(email="other@example.com", password_hash="hashed")
    session.add(other_user)
    session.flush()
    session.add_all(docs)
    session.add(_make_document(other_user.id, "projects/acme/contracts", "should-hide.pdf", 20))
    session.commit()

    resp = test_client.get("/documents", params={"limit": 2, "offset": 0})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert len(data["items"]) == 2
    # Newest document should appear first thanks to descending created_at ordering.
    assert data["items"][0]["filename"] == "notes-c.pdf"
    assert data["items"][0]["path"] == "projects/beta/notes"
    assert data["items"][0]["size"] == 3000

    resp_filter = test_client.get("/documents", params={"path_prefix": "projects/acme"})
    assert resp_filter.status_code == 200
    filtered = resp_filter.json()
    assert filtered["total"] == 2
    assert all(item["path"].startswith("projects/acme") for item in filtered["items"])


def test_delete_document_cleans_up_storage_and_search(client, monkeypatch):
    test_client, session, user = client
    doc = _make_document(user.id, "archive", "delete-me.pdf", 0, size=4096)
    session.add(doc)
    session.commit()
    session.refresh(doc)

    deleted_keys = []
    deleted_ids = []

    def fake_delete_object(key):
        deleted_keys.append(key)

    def fake_os_delete(doc_id):
        deleted_ids.append(doc_id)

    monkeypatch.setattr("app.main.delete_object", fake_delete_object)
    monkeypatch.setattr("app.main.os_delete", fake_os_delete)

    resp = test_client.delete(f"/documents/{doc.id}")
    assert resp.status_code == 204
    assert deleted_keys == [doc.s3_key]
    assert deleted_ids == [str(doc.id)]

    with TestingSessionLocal() as check_session:
        assert check_session.get(Document, doc.id) is None
