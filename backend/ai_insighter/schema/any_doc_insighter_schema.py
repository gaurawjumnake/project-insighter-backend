"""
DocumentInsight model
─────────────────────
Stores markdown insights generated from uploaded documents.
One row per uploaded document — multiple rows per entity supported.

Migration (Alembic or raw SQL):

    CREATE TABLE document_insights (
        id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        entity_type      VARCHAR(50)  NOT NULL,   -- 'project' | 'account' | 'pe'
        entity_id        UUID         NOT NULL,
        file_name        TEXT         NOT NULL,
        context_hint     TEXT,
        insight_markdown TEXT         NOT NULL,
        generated_at     TIMESTAMPTZ  NOT NULL DEFAULT now()
    );

    CREATE INDEX idx_document_insights_entity
        ON document_insights (entity_type, entity_id);
"""
import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone

from backend.db.base import Base

class DocumentInsight(Base):
    __tablename__ = "document_insights"

    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type      = Column(String(50), nullable=False)   # project | account | pe
    entity_id        = Column(UUID(as_uuid=True), nullable=False)
    file_name        = Column(Text, nullable=False)
    context_hint     = Column(Text, nullable=True)
    insight_markdown = Column(Text, nullable=False)
    generated_at     = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return (
            f"<DocumentInsight id={self.id} "
            f"entity={self.entity_type}/{self.entity_id} "
            f"file={self.file_name}>"
        )