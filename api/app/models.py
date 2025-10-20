import uuid
from sqlalchemy import Column, String, DateTime, Text, JSON, Enum, Integer, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .db import Base
class DocStatus(str, PyEnum):
    NEW="NEW"; PROCESSING="PROCESSING"; READY="READY"; FAILED="FAILED"
class User(Base):
    __tablename__="users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
class Document(Base):
    __tablename__="documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(String(512), nullable=False)
    path = Column(String(1024), nullable=True)
    content_type = Column(String(128), nullable=True)
    size = Column(Integer, nullable=True)
    bucket = Column(String(128), nullable=False)
    s3_key = Column(String(2048), nullable=False)
    status = Column(Enum(DocStatus), nullable=False, default=DocStatus.NEW)
    title = Column(String(512), nullable=True)
    meta = Column("metadata", JSON, nullable=True)
    text_excerpt = Column(Text, nullable=True)
    owner_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    owner = relationship("User")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
class ShareLink(Base):
    __tablename__="share_links"
    token = Column(String(64), primary_key=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    document = relationship("Document")
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    password_hash = Column(String(255), nullable=True)
