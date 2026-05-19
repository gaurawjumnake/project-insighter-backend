"""
Document Insights API Router
─────────────────────────────
Endpoints:
    POST /api/v1/insights/document/{entity_type}/{entity_id}
        — upload document, parse, generate markdown insights, persist

    GET  /api/v1/insights/document/{entity_type}/{entity_id}
        — retrieve all stored document insights for an entity

entity_type: "project" | "account" | "pe"

Insights stored in a separate document_insights table — supports
multiple documents per entity.
"""

import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from backend.db.session import get_db
from backend.utitlites.doc_importer import import_and_save_document
from backend.doc_insighter.tools.app_logger import Logger
from backend.utitlites.llm_models import llm
from backend.ai_insighter.services.any_data_insighter import DocumentInsightService

from backend.ai_insighter.schema.any_doc_insighter_schema import DocumentInsight

load_dotenv()
log = Logger()

TEMP_DIR = Path(os.getenv("TEMP_DIR", "/tmp"))
TEMP_DIR.mkdir(parents=True, exist_ok=True)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}

VALID_ENTITY_TYPES = {"project", "account", "pe"}

router = APIRouter(prefix="/api/v1/insights/document", tags=["Document Insights"])


class DocumentInsightGenerationResponse(BaseModel):
    status: str
    entity_type: str
    entity_id: str
    document_insight_id: Optional[str] = None
    file_name: Optional[str] = None
    insight_markdown: Optional[str] = None
    generated_at: Optional[str] = None
    error: Optional[str] = None


class DocumentInsightRecord(BaseModel):
    document_insight_id: str
    file_name: str
    context_hint: Optional[str] = None
    insight_markdown: str
    generated_at: str


class DocumentInsightListResponse(BaseModel):
    status: str
    entity_type: str
    entity_id: str
    total: int
    insights: List[DocumentInsightRecord]



def _validate_entity_type(entity_type: str) -> None:
    if entity_type not in VALID_ENTITY_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid entity_type '{entity_type}'. Must be one of: {VALID_ENTITY_TYPES}"
        )


def _validate_uuid(raw_id: str, label: str) -> UUID:
    try:
        return UUID(raw_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {label}. Must be a valid UUID. Got: {raw_id}"
        )


def _validate_file(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Supported: {SUPPORTED_EXTENSIONS}"
        )



@router.post(
    "/{entity_type}/{entity_id}",
    response_model=DocumentInsightGenerationResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def generate_document_insights(
    entity_type: str,
    entity_id: str,
    file: UploadFile = File(...),
    context_hint: Optional[str] = None,
    db: Session = Depends(get_db),
) -> DocumentInsightGenerationResponse:
    """
    Upload a document, parse it, and generate markdown insights.

    - entity_type: "project" | "account" | "pe"
    - entity_id:   UUID of the linked entity
    - file:        PDF, DOCX, TXT, or MD
    - context_hint: Optional free-text e.g. "Q1 review for Acme Corp"

    Flow:
      1. Validate inputs
      2. Parse document using import_and_save_document
      3. Run DocumentInsightService → markdown
      4. Persist to document_insights table
    """
    _validate_entity_type(entity_type)
    _validate_uuid(entity_id, "entity_id")
    _validate_file(file)

    log.log_info(
        f"Document insight requested — entity: {entity_type}/{entity_id} "
        f"file: {file.filename}"
    )

    try:
        # Step 1 — Parse document using existing import utility
        # Returns parsed text via the process_function pattern
        parse_result = await import_and_save_document(
            file=file,
            account_id=None,  # type:ignore      
            temp_dir=TEMP_DIR,
            success_dir=TEMP_DIR,
            failed_dir=TEMP_DIR,
            import_function=_parse_document_text,  
            db=db,
            dry_run=False,
            document_type="INSIGHT_DOC",
        )

        document_text = parse_result.get("parsed_text", "")

        if not document_text:
            raise HTTPException(
                status_code=400,
                detail="Document parsing returned no content."
            )

        # Step 2 — Generate markdown insights
        service = DocumentInsightService()
        insight_markdown = service.analyse(
            document_text = document_text,
            file_name     = file.filename or "uploaded_document",
            context_hint  = context_hint or f"Document linked to {entity_type} {entity_id}",
        )

        # Step 3 — Persist to document_insights table
        record = DocumentInsight(
            entity_type      = entity_type,
            entity_id        = entity_id,
            file_name        = file.filename,
            context_hint     = context_hint,
            insight_markdown = insight_markdown,
            generated_at     = datetime.now(timezone.utc),
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        return DocumentInsightGenerationResponse(
            status               = "success",
            entity_type          = entity_type,
            entity_id            = entity_id,
            document_insight_id  = str(record.id),
            file_name            = file.filename,
            insight_markdown     = str(insight_markdown),
            generated_at         = record.generated_at.isoformat(),
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log.log_error(f"Error generating document insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{entity_type}/{entity_id}",
    response_model=DocumentInsightListResponse,
)
def retrieve_document_insights(
    entity_type: str,
    entity_id: str,
    db: Session = Depends(get_db),
) -> DocumentInsightListResponse:
    """
    Retrieve all stored document insights for an entity.
    Returns newest first. Multiple documents per entity are supported.
    """
    _validate_entity_type(entity_type)
    _validate_uuid(entity_id, "entity_id")

    records = (
        db.query(DocumentInsight)
        .filter(
            DocumentInsight.entity_type == entity_type,
            DocumentInsight.entity_id   == entity_id,
        )
        .order_by(DocumentInsight.generated_at.desc())
        .all()
    )

    return DocumentInsightListResponse(
        status      = "success",
        entity_type = entity_type,
        entity_id   = entity_id,
        total       = len(records),
        insights    = [
            DocumentInsightRecord(
                document_insight_id = str(r.id),
                file_name           = str(r.file_name),
                context_hint        = str(r.context_hint),
                insight_markdown    = str(r.insight_markdown),
                generated_at        = r.generated_at.isoformat(),
            )
            for r in records
        ],
    )


# Passed as import_function to import_and_save_document.
# Replace body with your actual parser call.

async def _parse_document_text(file_path: str, db: Session, **kwargs) -> dict:
    """
    Extracts plain text from a document file.
    Swap this body for your existing LlamaParse or doc parser call.

    Must return: {"parsed_text": "<extracted text>"}
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        return {"parsed_text": text}
    except Exception as e:
        log.log_error(f"Document parse error: {e}")
        return {"parsed_text": ""}