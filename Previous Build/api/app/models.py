import uuid
from sqlalchemy import Column, String, DateTime, Text, JSON, Enum, Integer
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum as PyEnum

from .db import Base

class DocStatus(str, PyEnum):
    NEW = "NEW"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(512), nullable=False)
    content_type = Column(String(128), nullable=True)
    size = Column(Integer, nullable=True)

    bucket = Column(String(128), nullable=False)
    s3_key = Column(String(1024), nullable=False)

    status = Column(Enum(DocStatus), nullable=False, default=DocStatus.NEW)
    title = Column(String(512), nullable=True)
    metadata = Column(JSON, nullable=True)
    text_excerpt = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
