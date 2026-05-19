from sqlalchemy.orm import Session
from uuid import UUID, uuid4
from typing import List, Optional, Any
from backend.finance.app.models.private_equity import PrivateEquity
from backend.finance.app.schemas.private_equity import PrivateEquityCreate, PrivateEquityUpdate
from backend.doc_insighter.tools.app_logger import Logger

log = Logger()

def get_private_equity(db: Session, pe_id: UUID) -> Optional[PrivateEquity]:
    """Retrieve a single Private Equity record by ID."""
    return db.query(PrivateEquity).filter(PrivateEquity.id == pe_id).first()

def get_private_equities(db: Session, skip: int = 0, limit: int = 100) -> List[PrivateEquity]:
    """Retrieve a list of Private Equity records."""
    return db.query(PrivateEquity).offset(skip).limit(limit).all()

def create_private_equity(db: Session, pe_in: PrivateEquityCreate) -> PrivateEquity:
    """Create a new Private Equity record."""
    pe = PrivateEquity(
        id=uuid4(),
        **pe_in.model_dump()
    )
    db.add(pe)
    db.commit()
    db.refresh(pe)
    log.log_info(f"Private Equity created: {pe.name} ({pe.id})")
    return pe

def update_private_equity(db: Session, pe_id: UUID, pe_in: PrivateEquityUpdate) -> Optional[PrivateEquity]:
    """Update an existing Private Equity record."""
    pe = get_private_equity(db, pe_id)
    if not pe:
        return None
    
    update_data = pe_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pe, key, value)
    
    db.commit()
    db.refresh(pe)
    log.log_info(f"Private Equity updated: {pe.name} ({pe.id})")
    return pe

def delete_private_equity(db: Session, pe_id: UUID) -> bool:
    """Delete a Private Equity record."""
    pe = get_private_equity(db, pe_id)
    if not pe:
        return False
    
    db.delete(pe)
    db.commit()
    log.log_info(f"Private Equity deleted: {pe.name} ({pe.id})")
    return True
