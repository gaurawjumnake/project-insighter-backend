from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from pydantic import BaseModel
from typing import Optional, Dict, List
from pathlib import Path
import os
from sqlalchemy.orm import Session
from uuid import UUID
from backend.app.db.session import get_db
from backend.utitlites.doc_importer import import_and_save_document
from backend.doc_insighter.services.sow import process_document, get_account_document
from backend.doc_insighter.tools.app_logger import Logger
log = Logger()
from dotenv import load_dotenv

load_dotenv()
supported_extensions = os.getenv("SUPPORTED_DOC_TYPE_EXTENSIONS")

TEMP_DIR = Path(os.getenv("TEMP_DIR"))
PROJECT_DOCUMENT_DIR = Path(os.getenv("PROJECT_DOCUMENT_DIR"))
PROJECT_FAILED_DIR = Path(os.getenv("PROJECT_FAILED_DIR"))

for path in[TEMP_DIR, PROJECT_DOCUMENT_DIR, PROJECT_FAILED_DIR]:
    path.mkdir(parents=True, exist_ok=True)

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

@router.post("/import_sow/{account_id}", response_model=ImportResponse)
async def import_sow_document(
    account_id: UUID,
    file: UploadFile = File(...),
    dry_run: bool = False,  
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_extension = Path(file.filename).suffix.lower()
     
    if file_extension not in supported_extensions: # type:ignore
        raise HTTPException(status_code=400, detail=f"Invalid file format '{file_extension}'")

    if not account_id:
        raise HTTPException(status_code=400, detail="account_id is required")

    try:
        account_success_dir = PROJECT_DOCUMENT_DIR / str(account_id)
        account_success_dir.mkdir(parents=True, exist_ok=True)
        
        account_failed_dir = PROJECT_FAILED_DIR / str(account_id)
        account_failed_dir.mkdir(parents=True, exist_ok=True)
        
        result = await import_and_save_document(
            file=file,
            account_id=account_id,
            temp_dir=TEMP_DIR,
            success_dir=account_success_dir,
            failed_dir=account_failed_dir,
            import_function=process_document,
            db=db,
            dry_run=dry_run,
            document_type="SOW"
        )
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        log.log_error(f"Unexpected error in import_sow_document: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/sow/{account_id}", response_model=None)
async def get_sow_document(
    account_id: UUID,
    db: Session = Depends(get_db)
):
    document_type = "sow"
    try:
        doc = get_account_document(db, account_id, document_type) # type:ignore
        
        if not doc:
            raise HTTPException(status_code=404, detail=f"No SOW document found for account {account_id}")
        
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
        raise HTTPException(status_code=500, detail=f"Failed to retrieve document: {str(e)}")

@router.delete("/sow/{account_id}", response_model=None)
async def delete_sow_document(
    account_id: UUID,
    db: Session = Depends(get_db)
):
    document_type = "sow"
    try:
        doc = get_account_document(db, account_id, document_type) # type:ignore
        
        if not doc:
            raise HTTPException(status_code=404, detail=f"No SOW document found for account {account_id}")
        
        db.delete(doc)
        db.commit()
        
        return {
            "message": "SOW document deleted successfully",
            "document_id": str(doc.id),
            "account_id": str(account_id)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")