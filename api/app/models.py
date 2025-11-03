import uuid
from sqlalchemy import Column, String, DateTime, Text, JSON, Enum, Integer, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .db import Base

class DocStatus(str, PyEnum):
    NEW="NEW"; PROCESSING="PROCESSING"; READY="READY"; FAILED="FAILED"

class UserRole(str, PyEnum):
    ADMIN="admin"; EDITOR="editor"; VIEWER="viewer"

class User(Base):
    __tablename__="users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.EDITOR)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    display_name = Column(String(255), nullable=True)
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
class Folder(Base):
    __tablename__="folders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = Column(String(1024), nullable=False)
    name = Column(String(255), nullable=False)
    parent_path = Column(String(1024), nullable=True)
    owner_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
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

class UserInvitation(Base):
    __tablename__="user_invitations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, index=True)
    invited_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    inviter = relationship("User", foreign_keys=[invited_by])
    role = Column(Enum(UserRole), nullable=False, default=UserRole.VIEWER)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DocumentShare(Base):
    __tablename__="document_shares"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    document = relationship("Document")
    shared_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    sharer = relationship("User", foreign_keys=[shared_by])
    shared_with = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    recipient = relationship("User", foreign_keys=[shared_with])
    permission = Column(String(20), nullable=False, default='view')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class FolderShare(Base):
    __tablename__="folder_shares"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    folder_path = Column(String(500), nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", foreign_keys=[owner_id])
    shared_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    sharer = relationship("User", foreign_keys=[shared_by])
    shared_with = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    recipient = relationship("User", foreign_keys=[shared_with])
    permission = Column(String(20), nullable=False, default='view')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Favorite(Base):
    __tablename__="favorites"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    document = relationship("Document")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DocumentVersion(Base):
    __tablename__="document_versions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    document = relationship("Document")
    version_number = Column(Integer, nullable=False)
    s3_key = Column(String(2048), nullable=False)
    filename = Column(String(512), nullable=False)
    size = Column(Integer, nullable=True)
    content_type = Column(String(128), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    creator = relationship("User")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    comment = Column(Text, nullable=True)
