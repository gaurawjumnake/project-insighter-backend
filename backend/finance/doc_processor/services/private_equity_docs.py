from sqlalchemy.orm import Session, joinedload
from sqlalchemy import UUID
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone, timedelta
from backend.doc_insighter.core.extraction_pipeline import ProcessProjectDocument
from backend.doc_insighter.core.document_kpi_prompts import PrivateEquityDocs
from backend.doc_insighter.tools.app_logger import Logger
from backend.finance.app.models.private_equity_document import PrivateEquityDocument
from backend.finance.app.models.private_equity import PrivateEquity

log = Logger()

# IST timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

def get_pe_document(db: Session, pe_id: UUID, document_type: str) -> Optional[PrivateEquityDocument]:
    """Retrieve a single PE document by PE ID and type."""
    return db.query(PrivateEquityDocument).filter(
        PrivateEquityDocument.pe_id == pe_id,
        PrivateEquityDocument.document_type.ilike(document_type.lower())
    ).first()

def process_pe_document(
    db: Session, 
    file_path: Path, 
    pe_id: UUID, 
    document_type: str, 
    dry_run: bool = False
) -> dict[str, Any]:
    """
    Process PE document (company_capabilities or pe_details) and return summary dict.
    
    Args:
        db: Database session
        file_path: Path to the uploaded file
        pe_id: UUID of the Private Equity entity
        document_type: 'company_capabilities' or 'pe_details'
        dry_run: If True, only validates the file
    """
    
    # Select prompt based on document type
    if document_type.lower() == "company_capabilities":
        prompt = PrivateEquityDocs.company_capabilities_prompt
        db_doc_type = "company_capabilities"
    elif document_type.lower() == "pe_details":
        prompt = PrivateEquityDocs.pe_details_prompt
        db_doc_type = "pe_details"
    else:
        return {
            "errors": [f"Invalid document type: {document_type}"],
            "records_processed": 0,
            "records_created": 0
        }

    if not file_path or not Path(file_path).exists():
        log.log_debug(f"File path not found - {file_path}")
        return {
            "errors": [f"Document file not found: {file_path}"],
            "records_processed": 0,
            "records_created": 0
        }
    
    # Initialize processor with specific prompt
    doc_processor = ProcessProjectDocument(prompt, doc_name=db_doc_type)
    
    content = doc_processor.run_doc_processor(file_path)
    if not content:
        log.log_error(f"Unable to extract insights from document - {file_path}")
        content = ""

    if dry_run:
        return {
            "errors": [],
            "records_processed": 1,
            "records_created": 0,
            "message": "Dry run successful - document validated"
        }
    
    try:
        existing_doc = get_pe_document(db, pe_id, db_doc_type)
        
        if existing_doc:
            existing_doc.content = content
            existing_doc.file_name = file_path.name
            doc_data = existing_doc
            operation = "updated"
            records_created = 0
        else:
            ist_time = datetime.now(IST).replace(tzinfo=None)
            doc_data = PrivateEquityDocument(
                id=uuid4(),
                pe_id=pe_id,
                content=content,
                document_type=db_doc_type,
                file_name=file_path.name,
                created_at=ist_time
            )
            db.add(doc_data)
            operation = "created"
            records_created = 1
        
        db.commit()
        db.refresh(doc_data)

        log.log_info(f"PE File ({db_doc_type}) processed successfully and {operation} in db")
        
        return {
            "errors": [],
            "records_processed": 1,
            "records_created": records_created,
            "document_id": str(doc_data.id),
            "operation": operation,
            "message": f"Private Equity {db_doc_type} document {operation} successfully"
        }
        
    except IntegrityError as e:
        db.rollback()
        log.log_warning(f"File not processed correctly. Error message - {e}")
        return {
            "errors": [f"Database integrity error: {str(e)}"],
            "records_processed": 1,
            "records_created": 0
        }
    except Exception as e:
        db.rollback()
        log.log_error(f"Unexpected error processing PE {db_doc_type}: {e}")
        return {
            "errors": [f"Processing error: {str(e)}"],
            "records_processed": 1,
            "records_created": 0
        }
