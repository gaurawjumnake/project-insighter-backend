# PHASE 3: Code Generation / Update

**Tokens:** ~300-500 | **Duration:** 45-60 min | **Owner:** @api-dev OR @ai-arch  
**Gate:** ⏸️ WAIT_FOR_APPROVAL

---

## 📋 INPUT

- Task breakdown from PHASE 2
- Codebase conventions (PATTERNS.md, reference implementations)
- Approved tasks (T1, T2, T3, etc.)

---

## 🎯 ACTIONS

1. **Generate code ONLY for approved tasks** (don't exceed scope)
2. **Follow existing repo patterns** (DI, layered architecture, naming)
3. **Include comprehensive error handling** (don't skip validation)
4. **Add type hints + docstrings** (required)
5. **Validate against Pydantic schemas** (for API changes)

---

## ✅ REQUIRED CHECKLIST

Before generating code, verify:

- [ ] Task scope clear (what files? what lines of code?)
- [ ] Reference pattern identified (find similar code in repo)
- [ ] Error handling strategy planned (what can fail?)
- [ ] Type hints ready (function signatures, return types)
- [ ] Docstrings prepared (OpenAPI auto-generation)
- [ ] No hardcoded values (use config.py)
- [ ] No secrets in code (use environment variables)

---

## 📤 OUTPUT (Code + Diff Format)

```python
# file: backend/finance/app/schemas/account.py
# Task: T1

from pydantic import BaseModel
from typing import Optional

class AccountCreate(BaseModel):
    """Schema for creating a new Account"""
    name: str
    organization_id: int
    revenue_tier: Optional[str] = None
    new_field: Optional[str] = None  # ← NEW FIELD
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Acme Corp",
                "organization_id": 1,
                "revenue_tier": "enterprise",
                "new_field": "custom metadata"
            }
        }


# file: backend/finance/app/models/account.py
# Task: T2

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from backend.db.base import Base

class Account(Base):
    """SQLAlchemy model for Account entity"""
    __tablename__ = "account"
    
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(255), nullable=False)
    organization_id: int = Column(Integer, ForeignKey("organization.id"), nullable=False)
    revenue_tier: str = Column(String(50), nullable=True)
    new_field: str = Column(String(255), nullable=True)  # ← NEW COLUMN
    created_at: datetime = Column(DateTime, default=datetime.utcnow)


# file: backend/finance/app/services/account.py
# Task: T3

class AccountService:
    """Business logic for Account operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, req: AccountCreate) -> Account:
        """
        Create a new Account.
        
        Args:
            req: AccountCreate schema with name, organization_id, etc.
            
        Returns:
            Created Account instance
            
        Raises:
            ValueError: If organization_id doesn't exist
        """
        # Validate organization exists
        org = self.db.query(Organization).filter_by(id=req.organization_id).first()
        if not org:
            raise ValueError(f"Organization {req.organization_id} not found")
        
        # Create account
        account = Account(
            name=req.name,
            organization_id=req.organization_id,
            revenue_tier=req.revenue_tier,
            new_field=req.new_field  # ← HANDLE NEW FIELD
        )
        
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        
        return account
```

---

## 🏗️ ARCHITECTURAL PRINCIPLES

**Always follow these patterns:**

1. **Layered Architecture** (API → Service → Repository → ORM)
   - API layer: validation, serialization
   - Service layer: business logic, orchestration
   - Repository layer: data queries
   - ORM layer: SQLAlchemy models

2. **Dependency Injection** (FastAPI Depends pattern)
   - Never hardcode database sessions
   - Use Depends(get_db) for session injection

3. **Error Handling** (specific exceptions, not generic)
   - Custom exceptions (AppException)
   - HTTPException with specific codes (400, 404, 422, 500)
   - Never bare except:

4. **Type Safety** (full type hints)
   - Function signatures must have types
   - Return types required
   - Use Optional[] for nullable fields

5. **Pydantic Validation** (schemas for all inputs)
   - Request schemas (input validation)
   - Response schemas (output serialization)
   - Field examples for OpenAPI docs

---

## 🚨 CODE QUALITY GATES

Code generation FAILS if:

- ❌ No error handling (missing try/except, validation)
- ❌ Missing type hints (function signature without return type)
- ❌ Hardcoded secrets (passwords, API keys in code)
- ❌ No docstrings (especially for public APIs)
- ❌ Bare except: (must catch specific exceptions)
- ❌ N+1 queries (unoptimized SQL patterns)
- ❌ Not following PATTERNS.md

---

## 📞 ESCALATION

If code generation faces issues:

- **Pattern not found:** Ask for manual pattern reference
- **Scope mismatch:** Revert to PHASE 2, refine task
- **Architectural conflict:** Consult PATTERNS.md or [PROJECT_CONTEXT.md](../../../../PROJECT_CONTEXT.md)
- **Token budget exceeded:** Compress code or extend budget

---

## 🔗 NEXT STEP

→ Upon approval, proceed to **PHASE 4: Unit Test Generation** (`phases/PHASE-4-TESTING.md`)
