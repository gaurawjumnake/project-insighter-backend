# Codebase Patterns & Best Practices

Extracted from graphify analysis and code review. Reference these patterns when generating code or refactoring.

---

## 🏗️ ARCHITECTURAL PATTERNS

### Pattern 1: Layered Architecture (API → Service → Repository → ORM)

**Structure:**
```
API Layer (FastAPI routes + validation)
    ↓
Service Layer (business logic, orchestration)
    ↓
Repository Layer (data access, queries)
    ↓
ORM Layer (SQLAlchemy models)
    ↓
Database (PostgreSQL)
```

**Example: Account CRUD**
```python
# API Layer: backend/finance/app/api/account.py
@router.post("/", response_model=AccountOut)
async def create_account(req: AccountCreate, db: Session = Depends(get_db)):
    service = AccountService(db)
    return service.create(req)

# Service Layer: backend/finance/app/services/account.py
class AccountService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, req: AccountCreate) -> Account:
        # Business logic: validation, defaults, side effects
        account = Account(**req.dict())
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

# Model Layer: backend/finance/app/models/account.py
class Account(Base):
    __tablename__ = "account"
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(255), nullable=False)
    # ... relationships
```

**When to use:** Always structure new features this way (don't put business logic in routes)

---

### Pattern 2: Dependency Injection (FastAPI Depends)

**For database sessions:**
```python
from fastapi import Depends
from backend.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Usage in routes
@router.get("/")
async def list_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()
```

**For authentication (future):**
```python
def get_current_user(token: str = Header(...)) -> User:
    # Validate token, return user
    return User(id=user_id, email=email)

@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
```

**When to use:** Always inject dependencies (never global variables or imports)

---

### Pattern 3: Error Handling with Custom Exceptions

**Define custom exceptions:**
```python
# backend/finance/app/exceptions.py
class AccountNotFoundError(Exception):
    pass

class InvalidRevenueData(Exception):
    pass

# Use in service
class AccountService:
    def get_by_id(self, account_id: int) -> Account:
        account = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise AccountNotFoundError(f"Account {account_id} not found")
        return account

# Handle in route
from fastapi import HTTPException

@router.get("/{account_id}", response_model=AccountOut)
async def get_account(account_id: int, db: Session = Depends(get_db)):
    try:
        service = AccountService(db)
        return service.get_by_id(account_id)
    except AccountNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
```

**When to use:** Always catch specific exceptions, never bare `except:`

---

### Pattern 4: Async/Await for I/O-Bound Operations

**Async routes:**
```python
@router.post("/async-process")
async def process_document_async(req: DocumentProcessRequest, db: Session = Depends(get_db)):
    # Start async task, return immediately
    job_id = str(uuid.uuid4())
    asyncio.create_task(background_process(job_id, req, db))
    return {"job_id": job_id, "status": "processing"}

async def background_process(job_id: str, req: DocumentProcessRequest, db: Session):
    # Long-running I/O (S3, LLM calls, DB queries)
    try:
        result = await call_llm(req.prompt)
        store_result(job_id, result, db)
    except Exception as e:
        logger.error(f"Job {job_id} failed", exc_info=e)

# Client polls for result
@router.get("/async-process/{job_id}")
async def get_async_result(job_id: str, db: Session = Depends(get_db)):
    result = db.query(AsyncJob).filter(AsyncJob.id == job_id).first()
    return {"status": result.status, "result": result.result if result.completed else None}
```

**When to use:** Always use async for S3, LLM, external API calls (don't block request thread)

---

## 📝 DATA VALIDATION PATTERNS

### Pattern 1: Pydantic BaseModel with Examples

**Request schema:**
```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class AccountCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=255, description="Account name")
    organization_id: int = Field(..., gt=0, description="Parent organization ID")
    revenue_tier: Optional[str] = Field(default="standard", description="Pricing tier")
    
    @validator('name')
    def name_alphanumeric(cls, v):
        if not v.replace(' ', '').isalnum():
            raise ValueError('Account name must be alphanumeric')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Acme Corp",
                "organization_id": 1,
                "revenue_tier": "premium"
            }
        }
```

**Response schema:**
```python
class AccountOut(BaseModel):
    id: int
    name: str
    organization_id: int
    revenue_tier: str
    created_at: datetime
    
    class Config:
        orm_mode = True  # Convert SQLAlchemy models to Pydantic
```

**When to use:** Every API input/output must have Pydantic validation

---

### Pattern 2: SQLAlchemy Model with Relationships

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="accounts")
    projects = relationship("Project", back_populates="account", cascade="all, delete-orphan")
    documents = relationship("AccountDocument", back_populates="account")
    
    # Useful for API responses
    def __repr__(self):
        return f"<Account {self.id}: {self.name}>"
```

**When to use:** Define relationships explicitly with back_populates for clarity

---

## 🔐 LOGGING & MONITORING PATTERNS

### Pattern 1: Structured Logging

```python
from backend.doc_insighter.tools.app_logger import get_logger

logger = get_logger(__name__)

# Usage in service
class AccountService:
    def create(self, req: AccountCreate):
        logger.info("Creating account", extra={
            "organization_id": req.organization_id,
            "account_name": req.name
        })
        
        try:
            account = Account(**req.dict())
            self.db.add(account)
            self.db.commit()
            
            logger.info("Account created successfully", extra={
                "account_id": account.id
            })
            return account
        
        except IntegrityError as e:
            logger.error("Account creation failed - duplicate name", extra={
                "account_name": req.name,
                "error": str(e)
            })
            raise AccountAlreadyExistsError(req.name)
```

**When to use:** Log important state changes, errors, and performance events

---

## 🤖 CREWAI PATTERNS

### Pattern 1: Agent Definition with Tools

```python
from crewai import Agent, Tool
from backend.utitlites.s3_storage import S3Client

# Define tool
def read_s3_document(s3_path: str) -> str:
    """Read document content from S3."""
    s3 = S3Client()
    return s3.download_file(s3_path)

s3_tool = Tool(
    name="s3_reader",
    func=read_s3_document,
    description="Read any document from S3 by path"
)

# Define agent with tool
researcher = Agent(
    role="Financial Researcher",
    goal="Extract key financial metrics from SOW documents",
    backstory="Expert in financial document analysis with 10+ years experience",
    tools=[s3_tool],
    verbose=True
)
```

**When to use:** Always define tools explicitly before assigning to agents

---

### Pattern 2: Task Definition with Dependencies

```python
from crewai import Task

extract_task = Task(
    description="Extract budget and timeline from SOW document at {doc_path}",
    expected_output="JSON with extracted budget_usd, timeline_months, resource_requirements",
    agent=researcher,
    output_file="extracted_kpis.json"
)

analyze_task = Task(
    description="Analyze extracted KPIs and flag risks: over-budget, timeline compression, etc.",
    expected_output="JSON with risk_list, severity_scores, recommendations",
    agent=analyzer,
    context=[extract_task]  # Depends on extract_task output
)
```

**When to use:** Chain tasks with context to pass outputs between agents

---

## 🗂️ DATABASE OPTIMIZATION PATTERNS

### Pattern 1: Query Optimization (Avoid N+1)

**❌ BAD: N+1 Query**
```python
accounts = db.query(Account).all()
for account in accounts:
    projects = db.query(Project).filter(Project.account_id == account.id).all()
    # 1 query for accounts + N queries for projects = N+1 queries
```

**✅ GOOD: Eager Loading**
```python
from sqlalchemy.orm import joinedload

accounts = db.query(Account).options(
    joinedload(Account.projects)
).all()
# 1 query with join, all projects loaded
```

**When to use:** Always eager load relationships when you need them

---

### Pattern 2: Materialized View for Analytics

```python
# One-time view creation
class AccountMetricsMV(Base):
    __tablename__ = "account_metrics_mv"
    __sync_to_db__ = False  # Don't auto-create
    
    account_id = Column(Integer, primary_key=True)
    total_revenue = Column(Float)
    project_count = Column(Integer)
    document_count = Column(Integer)
    updated_at = Column(DateTime)

# Usage in dashboards (much faster than JOIN)
metrics = db.query(AccountMetricsMV).filter(
    AccountMetricsMV.account_id == account_id
).first()
```

**When to use:** Use materialized views for read-heavy analytics (refresh daily/weekly)

---

## 🧪 TESTING PATTERNS

### Pattern 1: Fixture-Based Setup

```python
import pytest
from backend.db.session import SessionLocal

@pytest.fixture
def db():
    """Provide a test database session."""
    db = SessionLocal()
    yield db
    db.rollback()
    db.close()

@pytest.fixture
def sample_account(db):
    """Create a sample account for tests."""
    account = Account(name="Test Corp", organization_id=1)
    db.add(account)
    db.commit()
    return account

def test_get_account(db, sample_account):
    service = AccountService(db)
    result = service.get_by_id(sample_account.id)
    assert result.name == "Test Corp"
```

**When to use:** Use fixtures for reusable test data setup

---

### Pattern 2: Mock External Calls

```python
from unittest.mock import patch, MagicMock

def test_create_account_with_llm_enrichment():
    with patch('backend.utitlites.llm_models.get_llm_client') as mock_llm:
        mock_llm.return_value.agenerate.return_value = "enriched_description"
        
        service = AccountService(db)
        account = service.create(AccountCreate(name="Test", organization_id=1))
        
        assert account.description == "enriched_description"
        mock_llm.return_value.agenerate.assert_called_once()
```

**When to use:** Mock external API calls, LLM, S3 in unit tests

---

## 🚀 DEPLOYMENT PATTERNS

### Pattern 1: Environment-Based Configuration

```python
# backend/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    AZURE_OPENAI_API_KEY: str
    AWS_S3_BUCKET: str
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Usage
db_url = settings.DATABASE_URL  # From .env or env vars
```

**When to use:** Never hardcode credentials, always use config

---

### Pattern 2: Lambda Handler (Mangum)

```python
# main.py
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="Project Insighter Backend")

# Routes
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Lambda handler
handler = Mangum(app, lifespan="off")

# Local dev
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**When to use:** Use Mangum for AWS Lambda deployment, Uvicorn for local dev

---

## 📊 GRAPHIFY INSIGHTS (Applied Patterns)

| God Node | Pattern Applied |
|----------|-----------------|
| **Logger** (227 edges) | Structured logging everywhere (not just errors) |
| **Account** (61 edges) | Shared model across Finance/Sales (single source of truth) |
| **Project** (61 edges) | Relationships configured with cascade semantics |
| **LlamaCloudDocumentParser** (31 edges) | Shared Doc Insighter engine (not replicated) |
| **RevenueMaster** (50 edges) | Materialized view for analytics (AccountMetricsMV) |

---

**Version:** 1.0 | **Last Updated:** 2026-05-07  
**Sources:** Graphify (917 nodes, 42 communities) + Code Review
