from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from backend.app.models.stakeholder_details import StakeholderDetails
from backend.app.schemas.stakeholder_details import StakeholderDetailsCreate, StakeholderDetailsUpdate

class StakeholderDetailsService:
    """Service class for StakeholderDetails CRUD operations."""
    
    @staticmethod
    def create(db: Session, stakeholder_data: StakeholderDetailsCreate) -> StakeholderDetails:
        """Create a new stakeholder details entry."""
        db_stakeholder = StakeholderDetails(**stakeholder_data.model_dump())
        db.add(db_stakeholder)
        db.commit()
        db.refresh(db_stakeholder)
        return db_stakeholder
    
    @staticmethod
    def get_by_id(db: Session, stakeholder_id: UUID) -> Optional[StakeholderDetails]:
        """Get stakeholder details by ID."""
        return db.query(StakeholderDetails).filter(StakeholderDetails.id == stakeholder_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[StakeholderDetails]:
        """Get all stakeholder details with pagination."""
        return db.query(StakeholderDetails).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_account_id(db: Session, account_id: UUID) -> List[StakeholderDetails]:
        """Get all stakeholder details for a specific account."""
        return db.query(StakeholderDetails).filter(StakeholderDetails.account_id == account_id).all()
    
    @staticmethod
    def update(db: Session, stakeholder_id: UUID, stakeholder_data: StakeholderDetailsUpdate) -> Optional[StakeholderDetails]:
        """Update existing stakeholder details."""
        db_stakeholder = db.query(StakeholderDetails).filter(StakeholderDetails.id == stakeholder_id).first()
        if not db_stakeholder:
            return None
        
        # Update only provided fields
        update_data = stakeholder_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_stakeholder, field, value)
        
        db.commit()
        db.refresh(db_stakeholder)
        return db_stakeholder
    
    @staticmethod
    def delete(db: Session, stakeholder_id: UUID) -> bool:
        """Delete stakeholder details."""
        db_stakeholder = db.query(StakeholderDetails).filter(StakeholderDetails.id == stakeholder_id).first()
        if not db_stakeholder:
            return False
        
        db.delete(db_stakeholder)
        db.commit()
        return True
    
    @staticmethod
    def search_by_incumbency_strength(db: Session, incumbency_strength: str) -> List[StakeholderDetails]:
        """Search stakeholder details by incumbency strength."""
        return db.query(StakeholderDetails).filter(StakeholderDetails.incumbency_strength == incumbency_strength).all()