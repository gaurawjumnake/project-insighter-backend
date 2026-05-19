from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from backend.db.session import get_db
from backend.finance.app.schemas.private_equity import PrivateEquityCreate, PrivateEquityUpdate, PrivateEquityOut
from backend.finance.app.services import private_equity as pe_service
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

router = APIRouter(prefix="/private-equity", tags=["Private Equity"])

@router.post("/", response_model=PrivateEquityOut, status_code=status.HTTP_201_CREATED)
def create_pe(pe_in: PrivateEquityCreate, db: Session = Depends(get_db)):
    """Create a new Private Equity record."""
    try:
        return pe_service.create_private_equity(db, pe_in)
    except Exception as e:
        log.log_error(f"Error creating Private Equity: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create Private Equity")

@router.get("/", response_model=List[PrivateEquityOut])
def get_pes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve all Private Equity records."""
    try:
        return pe_service.get_private_equities(db, skip, limit)
    except Exception as e:
        log.log_error(f"Error retrieving Private Equities: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Private Equities")

@router.get("/{pe_id}", response_model=PrivateEquityOut)
def get_pe(pe_id: UUID, db: Session = Depends(get_db)):
    """Retrieve a single Private Equity record by ID."""
    pe = pe_service.get_private_equity(db, pe_id)
    if not pe:
        raise HTTPException(status_code=404, detail="Private Equity not found")
    return pe

@router.put("/{pe_id}", response_model=PrivateEquityOut)
def update_pe(pe_id: UUID, pe_in: PrivateEquityUpdate, db: Session = Depends(get_db)):
    """Update a Private Equity record."""
    pe = pe_service.update_private_equity(db, pe_id, pe_in)
    if not pe:
        raise HTTPException(status_code=404, detail="Private Equity not found")
    return pe

@router.delete("/{pe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pe(pe_id: UUID, db: Session = Depends(get_db)):
    """Delete a Private Equity record."""
    success = pe_service.delete_private_equity(db, pe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Private Equity not found")
    return None
