from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from pydantic import BaseModel
from typing import Optional, Dict, List
from pathlib import Path
import os
from sqlalchemy.orm import Session
from uuid import UUID
from backend.db.session import get_db
from backend.utitlites.doc_importer import import_and_save_document
from backend.finance.doc_processor.services.private_equity_docs import process_pe_document, get_pe_document
from backend.doc_insighter.tools.app_logger import Logger
from dotenv import load_dotenv

log = Logger()
load_dotenv()

supported_extensions = os.getenv("SUPPORTED_DOC_TYPE_EXTENSIONS", ".pdf,.docx,.doc,.txt")
TEMP_DIR = Path(os.getenv("TEMP_DIR", "/tmp"))
TEMP_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/document/pe", tags=["Private-Equity-Documents"])

class ImportResponse(BaseModel):
    errors: List[str] = []
    records_processed: int
    records_created: int
    uploaded_file: Optional[str] = None
    file_size_mb: Optional[float] = None
    import_status: str
    document_id: Optional[str] = None
    operation: Optional[str] = None
    message: Optional[str] = None

@router.post("/import/{pe_id}/{document_type}", response_model=ImportResponse)
async def import_pe_document(
    pe_id: UUID,
    document_type: str,
    file: UploadFile = File(...),
    dry_run: bool = False,
    db: Session = Depends(get_db)
):
    """
    Import Private Equity related documents.
    
    - **pe_id**: UUID of the Private Equity entity
    - **document_type**: 'company_capabilities' or 'pe_details'
    - **file**: Document file (PDF, DOCX, DOC, TXT)
    - **dry_run**: If True, validates file without saving to database
    """
    if document_type.lower() not in ["company_capabilities", "pe_details"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid document type. Must be 'company_capabilities' or 'pe_details'"
        )

    if not file.filename:
        raise HTTPException(
            status_code=400, 
            detail="No filename provided"
        )

    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in supported_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file format '{file_extension}'. Supported formats: {supported_extensions}"
        )

    try:
        def pe_wrapper(db, file_path, entity_id, dry_run):
            return process_pe_document(
                db=db,
                file_path=file_path,
                pe_id=entity_id,
                document_type=document_type,
                dry_run=dry_run
            )

        result = await import_and_save_document(
            file=file,
            account_id=pe_id, # Reusing account_id parameter for pe_id
            temp_dir=TEMP_DIR,
            success_dir=TEMP_DIR,
            failed_dir=TEMP_DIR,
            import_function=pe_wrapper,
            db=db,
            dry_run=dry_run,
            document_type=document_type.upper(),
            subfolder="pe"
        )
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Unexpected error in import_pe_document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/{pe_id}/{document_type}")
async def get_private_equity_document(
    pe_id: UUID,
    document_type: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve PE document insights.
    - **pe_id**: UUID of the PE entity
    - **document_type**: 'company_capabilities' or 'pe_details'
    """
    try:
        doc = get_pe_document(db, pe_id, document_type)
        
        if not doc:
            raise HTTPException(
                status_code=404,
                detail=f"No {document_type} document found for PE {pe_id}"
            )
        
        return {
            "document_id": str(doc.id),
            "pe_id": str(doc.pe_id),
            "content": doc.content,
            "document_type": doc.document_type,
            "file_name": doc.file_name,
            "created_at": doc.created_at.isoformat() if doc.created_at else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Error retrieving PE document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve document: {str(e)}"
        )

@router.delete("/{pe_id}/{document_type}")
async def delete_pe_document(
    pe_id: UUID,
    document_type: str,
    db: Session = Depends(get_db)
):
    """
    Delete PE document.
    - **pe_id**: UUID of the PE entity
    - **document_type**: 'company_capabilities' or 'pe_details'
    """
    try:
        doc = get_pe_document(db, pe_id, document_type)
        
        if not doc:
            raise HTTPException(
                status_code=404,
                detail=f"No {document_type} document found for PE {pe_id}"
            )
        
        db.delete(doc)
        db.commit()
        
        log.log_info(f"PE {document_type} document deleted for PE {pe_id}")
        
        return {
            "message": f"PE {document_type} document deleted successfully",
            "document_id": str(doc.id),
            "pe_id": str(pe_id)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log.log_error(f"Error deleting PE document: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {str(e)}"
        )
