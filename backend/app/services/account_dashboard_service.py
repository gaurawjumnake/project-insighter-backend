from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from backend.app.models.account_dashboard import AccountDashboard
from backend.app.schemas.account_dashboard import AccountDashboardCreate, AccountDashboardUpdate

class AccountDashboardService:
    """Service class for AccountDashboard CRUD operations."""
    
    @staticmethod
    def create(db: Session, account_data: AccountDashboardCreate) -> AccountDashboard:
        """Create a new account dashboard entry."""
        # Convert Pydantic model to SQLAlchemy model
        db_account = AccountDashboard(**account_data.model_dump())
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    
    @staticmethod
    def get_by_id(db: Session, account_id: UUID) -> Optional[AccountDashboard]:
        """Get account dashboard by ID."""
        return db.query(AccountDashboard).filter(AccountDashboard.account_id == account_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[AccountDashboard]:
        """Get all account dashboards with pagination."""
        return db.query(AccountDashboard).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, account_id: UUID, account_data: AccountDashboardUpdate) -> Optional[AccountDashboard]:
        """Update an existing account dashboard."""
        db_account = db.query(AccountDashboard).filter(AccountDashboard.account_id == account_id).first()
        if not db_account:
            return None
        
        # Exclude unset fields to allow partial updates
        update_data = account_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_account, field, value)
        
        db.commit()
        db.refresh(db_account)
        return db_account
    
    @staticmethod
    def delete(db: Session, account_id: UUID) -> bool:
        """Delete an account dashboard."""
        db_account = db.query(AccountDashboard).filter(AccountDashboard.account_id == account_id).first()
        if not db_account:
            return False
        
        db.delete(db_account)
        db.commit()
        return True

    @staticmethod
    def search_by_delivery_unit(db: Session, delivery_unit: str) -> List[AccountDashboard]:
        """Search accounts by delivery unit."""
        return db.query(AccountDashboard).filter(AccountDashboard.delivery_unit == delivery_unit).all()