# Skill: FastAPI Endpoint Scaffold

**Purpose:** Generate complete FastAPI endpoint with route, service, schema, and tests  
**Agent:** @api-dev  
**Duration:** 2-3 minutes

---

## QUERY PATTERN

```
@api-dev Generate {operation} endpoint for {entity}
where operation = [create, read, update, delete, list, search]
and entity = [Account, Project, Document, Revenue, ...]

Examples:
- Generate create endpoint for Document
- Generate list endpoint for Projects with filtering by account_id
- Generate update endpoint for Account with validation
```

---

## IMPLEMENTATION

### Step 1: Analyze Existing Patterns
Read reference implementation:
```python
# backend/finance/app/api/account.py
# backend/finance/app/services/account.py
```

### Step 2: Generate Endpoint
Create route file with:
- Request/response Pydantic schemas
- REST-compliant HTTP methods
- Full error handling (400, 404, 409, 422, 500)
- OpenAPI docstrings
- Type hints on all signatures

**Generated Code Template:**
```python
# backend/{module}/app/api/{resource}.py
@router.post("/", response_model=EntityOut, status_code=201)
async def create_entity(
    req: EntityCreate,
    db: Session = Depends(get_db)
) -> EntityOut:
    """Create new Entity with validation."""
    service = EntityService(db)
    try:
        return service.create(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Already exists")
```

### Step 3: Generate Service Layer
Create service class with:
- Business logic separate from route
- DB session management
- Error handling with custom exceptions

### Step 4: Generate Tests
Create pytest tests with:
- Happy path test
- 5+ error case tests
- Edge cases (empty, boundary values)
- Mock external dependencies

### Step 5: Validate & Document
- Verify OpenAPI spec generation
- Check type hints completeness
- Ensure tests pass

---

## SUCCESS METRICS

- ✅ Endpoint follows REST conventions
- ✅ Code quality ≥90% (SonarQube)
- ✅ Tests passing with ≥90% coverage
- ✅ OpenAPI docs auto-generated
- ✅ Type hints on all functions
- ✅ No hardcoded values (config-driven)
- ✅ Error handling covers 5+ scenarios

---

## HANDOFFS

- **To @ai-arch:** If endpoint needs AI logic ("Add ML model prediction")
- **To @data-analyst:** If schema impacts queries ("Optimize for reporting")

---

## ACCEPTANCE CHECKLIST

- [ ] Route created with HTTP method (POST, GET, PUT, DELETE)
- [ ] Request/response schemas defined with Pydantic
- [ ] Service layer handles business logic
- [ ] Error handling covers all common cases
- [ ] Tests have ≥90% code coverage
- [ ] Type hints on all function signatures
- [ ] Docstrings for OpenAPI documentation
- [ ] No validation skipped
- [ ] No global database connections

**Version:** 1.0 | Last Updated: 2026-05-07
