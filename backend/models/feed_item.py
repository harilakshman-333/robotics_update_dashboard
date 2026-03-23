import uuid
from datetime import datetime
from sqlalchemy import Column, String, Enum, Integer, Boolean, DateTime, JSON, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base
from enum import Enum as PyEnum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class SourceEnum(PyEnum):
    x = "x"
    gmail = "gmail"
    web = "web"

class FeedItem(Base):
    __tablename__ = "feed_items"
    __table_args__ = (UniqueConstraint("url", name="uq_feeditem_url"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[SourceEnum] = mapped_column(Enum(SourceEnum), nullable=False)
    raw_text: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    entities_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(MutableDict.as_mutable(JSON), nullable=True)
    relevance_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    enriched: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    enriched_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

class FeedItemOut(BaseModel):
    id: uuid.UUID
    url: str
    title: str
    source: str
    raw_text: str
    summary: Optional[str]
    category: Optional[str]
    sentiment: Optional[str]
    entities_json: Optional[Dict[str, Any]]
    relevance_score: Optional[int]
    enriched: bool
    created_at: datetime
    enriched_at: Optional[datetime]

    class Config:
        from_attributes = True
