from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from pydantic import BaseModel
from typing import Optional, Dict, List
from pathlib import Path
import os
from sqlalchemy.orm import Session
from uuid import UUID
from backend.db.session import get_db
from backend.utitlites.doc_importer import import_and_save_document
from backend.sales.doc_processor.services.other_docs import process_other_docs_document, get_account_document
from backend.sales.app.models.account_dashboard import AccountDashboard
from backend.doc_insighter.tools.app_logger import Logger
log = Logger()
from dotenv import load_dotenv

load_dotenv()
supported_extensions = os.getenv("SUPPORTED_DOC_TYPE_EXTENSIONS")

TEMP_DIR = Path(os.getenv("TEMP_DIR", "/tmp"))
TEMP_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/document", tags=["Account-Documents"])

class InputRequest(BaseModel):
    file_path:str

class ImportResponse(BaseModel):
    errors: List[str] =[]
    records_processed: int
    records_created: int
    uploaded_file: Optional[str] = None
    file_size_mb: Optional[float] = None
    import_status: str
    document_id: Optional[str] = None
    operation: Optional[str] = None
    message: Optional[str] = None

@router.post("/import_other_docs/{account_id}", response_model=ImportResponse)
async def import_other_docs_document(
    account_id: UUID,
    file: UploadFile = File(...),
    dry_run: bool = False,  
    db: Session = Depends(get_db)
):
    """
    Import Other document for an account.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_extension = Path(file.filename).suffix.lower()
     
    if file_extension not in supported_extensions: # type:ignore
        raise HTTPException(status_code=400, detail=f"Invalid file format '{file_extension}'. Supported formats: {supported_extensions}")

    if not account_id:
        raise HTTPException(status_code=400, detail="account_id is required")

    try:
        account_exists = (
            db.query(AccountDashboard.account_id)
            .filter(AccountDashboard.account_id == account_id)
            .first()
        )
        if not account_exists:
            raise HTTPException(
                status_code=404,
                detail=f"Account {account_id} not found in account_dashboard."
            )

        result = await import_and_save_document(
            file=file,
            account_id=account_id,
            temp_dir=TEMP_DIR,
            success_dir=TEMP_DIR,
            failed_dir=TEMP_DIR,
            import_function=process_other_docs_document,
            db=db,
            dry_run=dry_run,
            document_type="OTHER_DOCS"
        )

        if result.get("errors"):
            raise HTTPException(
                status_code=400,
                detail="; ".join([str(err) for err in result.get("errors", []) if err])
            )
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Unexpected error in import_other_docs_document: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/other_docs/{account_id}", response_model=None)
async def get_other_docs_document(
    account_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Retrieve Other document for an account.
    """
    document_type = "other_docs"
    try:
        doc = get_account_document(db, account_id, document_type) # type:ignore
        
        if not doc:
            raise HTTPException(status_code=404, detail=f"No document found for account {account_id}")
        
        return {
            "document_id": str(doc.id),
            "account_id": str(doc.account_id),
            "content": doc.content,
            "document_type": doc.document_type,
            "created_at": doc.created_at.isoformat() if doc.created_at else None # type:ignore
        }
    
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Error retrieving Other document: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve document: {str(e)}")

@router.delete("/other_docs/{account_id}", response_model=None)
async def delete_other_docs_document(
    account_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete Other document for an account.
    """
    document_type = "other_docs"
    try:
        doc = get_account_document(db, account_id, document_type) # type:ignore
        
        if not doc:
            raise HTTPException(status_code=404, detail=f"No document found for account {account_id}")
        
        db.delete(doc)
        db.commit()
        
        log.log_info(f"Other document deleted for account {account_id}")
        
        return {
            "message": "Other document deleted successfully",
            "document_id": str(doc.id),
            "account_id": str(account_id)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log.log_error(f"Error deleting Other document: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
