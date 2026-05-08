# Prompt: FastAPI Endpoint Design

**For:** Generating new FastAPI endpoints following project conventions  
**Used by:** @api-dev agent

---

## 🎯 OBJECTIVE

Generate FastAPI endpoints that are:
- Type-safe with full type hints
- Validated with Pydantic models
- Well-documented with OpenAPI
- Error-handling complete (happy path + 5 error cases minimum)
- Production-ready with tests

---

## 📋 CHECKLIST BEFORE GENERATING CODE

- [ ] Entity name is clear (Account, Project, Document, etc.)
- [ ] Operation is specified (create, read, update, delete, list, search)
- [ ] Input validation rules documented (required fields, constraints)
- [ ] Success response structure defined
- [ ] Error scenarios identified (404, 400, 409, 422, 500)
- [ ] Authentication requirements stated
- [ ] Cross-module dependencies checked (Finance/Sales/Insights)
- [ ] Existing patterns reviewed (similar endpoint in codebase)

---

## 🏗️ ENDPOINT STRUCTURE TEMPLATE

```python
# File: backend/{module}/app/api/{resource}.py

from fastapi import APIRouter, Depends, HTTPException, status
from backend.db.session import SessionLocal
from sqlalchemy.orm import Session
from backend.{module}.app.models import {Entity}
from backend.{module}.app.schemas import {EntityCreate}, {EntityOut}
from backend.{module}.app.services import {EntityService}
from backend.doc_insighter.tools.app_logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/{resources}", tags=["{Entity}"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@router.post("/", response_model={EntityOut}, status_code=status.HTTP_201_CREATED)
async def create_{resource}(
    req: {EntityCreate},
    db: Session = Depends(get_db)
) -> {EntityOut}:
    """
    Create a new {Entity}.
    
    **Request:**
    - Required fields: {list validation rules}
    
    **Response:**
    - 201: {Entity} created successfully
    - 400: Invalid input (validation error)
    - 409: Conflict (e.g., duplicate name)
    - 500: Server error
    
    **Example:**
    ```
    POST /api/v1/{resources}
    {
        "field1": "value1",
        "field2": "value2"
    }
    
    Response:
    {
        "id": 1,
        "field1": "value1",
        "created_at": "2026-05-07T10:00:00Z"
    }
    ```
    """
    logger.info(f"Creating {resource}", extra={"input": req.dict()})
    
    service = {EntityService}(db)
    try:
        result = service.create(req)
        logger.info(f"{Entity} created", extra={"id": result.id})
        return result
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError as e:
        logger.error(f"Integrity error: {e}")
        raise HTTPException(status_code=409, detail=f"{Entity} already exists")

# READ (single)
@router.get("/{id}", response_model={EntityOut})
async def get_{resource}(
    id: int,
    db: Session = Depends(get_db)
) -> {EntityOut}:
    """Get {Entity} by ID."""
    logger.info(f"Fetching {resource}", extra={"id": id})
    
    service = {EntityService}(db)
    result = service.get_by_id(id)
    
    if not result:
        logger.warning(f"{Entity} not found", extra={"id": id})
        raise HTTPException(status_code=404, detail=f"{Entity} {id} not found")
    
    return result

# READ (list with filters)
@router.get("/", response_model=list[{EntityOut}])
async def list_{resources}(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List {Entity}s with pagination."""
    logger.info(f"Listing {resources}", extra={"skip": skip, "limit": limit})
    
    service = {EntityService}(db)
    return service.list_all(skip=skip, limit=limit)

# UPDATE
@router.put("/{id}", response_model={EntityOut})
async def update_{resource}(
    id: int,
    req: {EntityUpdate},
    db: Session = Depends(get_db)
) -> {EntityOut}:
    """Update {Entity}."""
    logger.info(f"Updating {resource}", extra={"id": id})
    
    service = {EntityService}(db)
    existing = service.get_by_id(id)
    
    if not existing:
        raise HTTPException(status_code=404, detail=f"{Entity} {id} not found")
    
    try:
        result = service.update(id, req)
        logger.info(f"{Entity} updated", extra={"id": id})
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# DELETE
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{resource}(
    id: int,
    db: Session = Depends(get_db)
):
    """Delete {Entity}."""
    logger.info(f"Deleting {resource}", extra={"id": id})
    
    service = {EntityService}(db)
    if not service.delete(id):
        raise HTTPException(status_code=404, detail=f"{Entity} {id} not found")
    
    logger.info(f"{Entity} deleted", extra={"id": id})
```

---

## 🔍 VALIDATION RULES

**For request schemas:**
- Use `Field(...)` for all fields with constraints
- Use `@validator` for complex validations
- Include `Config.schema_extra` with example
- Never allow `None` without `Optional`

**For error handling:**
- 400: Bad request (validation error)
- 404: Not found (resource doesn't exist)
- 409: Conflict (duplicate, constraint violation)
- 422: Unprocessable entity (semantic error)
- 500: Server error (unexpected exception)

---

## 🧪 TESTING REQUIREMENTS

Every endpoint needs:
1. **Happy path test** — Valid input, 200/201 response
2. **Validation error test** — Invalid input, 400 response
3. **Not found test** — Valid format, missing resource, 404
4. **Conflict test** — Duplicate/constraint violation, 409
5. **Edge cases** — Empty list, boundary values, special characters

```python
# tests/finance/test_accounts.py
def test_create_account_success(db):
    req = AccountCreate(name="Acme Corp", organization_id=1)
    response = client.post("/api/v1/accounts", json=req.dict())
    assert response.status_code == 201

def test_create_account_missing_name(db):
    req = {"organization_id": 1}  # Missing name
    response = client.post("/api/v1/accounts", json=req)
    assert response.status_code == 422

def test_get_account_not_found(db):
    response = client.get("/api/v1/accounts/99999")
    assert response.status_code == 404
```

---

## ✅ ACCEPTANCE CRITERIA

- [ ] Endpoint follows REST conventions (GET, POST, PUT, DELETE)
- [ ] All inputs validated with Pydantic
- [ ] All outputs typed with response_model
- [ ] Errors caught and logged with context
- [ ] OpenAPI docs generated automatically (docstring + response_model)
- [ ] Tests cover happy path + all error cases
- [ ] Type hints on all function signatures
- [ ] Service layer handles business logic (not route handler)
- [ ] Logging included for debugging
- [ ] No hardcoded values (use config)

---

**Last Updated:** 2026-05-07
