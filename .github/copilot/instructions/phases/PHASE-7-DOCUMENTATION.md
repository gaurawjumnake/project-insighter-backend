# PHASE 7: Documentation

**Tokens:** ~100-150 | **Duration:** 20-30 min | **Owner:** @api-dev OR Orchestrator  
**Gate:** ⏸️ WAIT_FOR_APPROVAL

---

## 📋 INPUT

- Generated code from PHASE 3
- Test cases from PHASE 4
- Code review findings from PHASE 5
- Ticket description and acceptance criteria

---

## 🎯 ACTIONS

1. **Update inline comments** (clarify "why", not "what")
2. **Update docstrings** (module, class, function level)
3. **Update README / API docs** (usage examples)
4. **Add code examples** if new feature
5. **Update CHANGELOG** (if applicable)

---

## 📤 DOCUMENTATION OUTPUT

### 1. Inline Comments & Docstrings

```python
# GOOD: Explains WHY
def create_account(self, req: AccountCreate) -> Account:
    """
    Create a new Account with optional custom metadata tracking.
    
    This method validates organization ownership before creating
    the account to prevent data inconsistencies across Finance and
    Sales modules (Account is a shared god node with 61 edges).
    
    Args:
        req: AccountCreate schema containing:
            - name (required): Account name (1-255 chars)
            - organization_id (required): Parent organization
            - revenue_tier (optional): Account tier (enterprise, mid-market, etc.)
            - new_field (optional): Custom metadata for Q2 reporting
    
    Returns:
        Created Account instance with auto-generated ID and timestamps
    
    Raises:
        ValueError: If organization_id doesn't exist
        ValidationError: If data doesn't match schema
    
    Example:
        >>> req = AccountCreate(
        ...     name="Acme Corp",
        ...     organization_id=1,
        ...     new_field="Q2 metadata"
        ... )
        >>> service = AccountService(db)
        >>> account = service.create(req)
        >>> print(account.id)
        42
    """
    # Validate organization exists (prevents FK constraint errors downstream)
    org = self.db.query(Organization).filter_by(id=req.organization_id).first()
    if not org:
        raise ValueError(f"Organization {req.organization_id} not found")
    
    # Create account with all fields
    account = Account(...)
    
    return account


# BAD: Just restates the code
def create_account(self, req: AccountCreate) -> Account:
    """Create an account"""
    # Get organization
    org = self.db.query(Organization).filter_by(id=req.organization_id).first()
    # Check if org exists
    if not org:
        raise ValueError(...)
    # Create account
    account = Account(...)
    return account
```

### 2. README / API Documentation Update

```markdown
## Account Management

### Create Account

**Endpoint:** `POST /api/v1/accounts`

**Description:** Create a new account with optional custom metadata.

**Request Schema:**
```json
{
  "name": "Acme Corp",
  "organization_id": 1,
  "revenue_tier": "enterprise",
  "new_field": "Q2 metadata (optional)"
}
```

**Response Schema (201 Created):**
```json
{
  "id": 42,
  "name": "Acme Corp",
  "organization_id": 1,
  "revenue_tier": "enterprise",
  "new_field": "Q2 metadata",
  "created_at": "2026-05-07T10:30:00Z",
  "updated_at": "2026-05-07T10:30:00Z"
}
```

**Error Responses:**
- `400 Bad Request`: Missing required fields
- `404 Not Found`: Organization ID doesn't exist
- `422 Unprocessable Entity`: Validation failed (e.g., new_field > 255 chars)
- `500 Internal Server Error`: Server error

**Example using cURL:**
```bash
curl -X POST http://localhost:8000/api/v1/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corp",
    "organization_id": 1,
    "new_field": "Q2 reporting"
  }'
```

**Backward Compatibility:**
✅ `new_field` is optional (nullable) → Existing clients unaffected
✅ No breaking API changes
✅ Database column is nullable → No migration required

### Architecture

**Code Changes:** 3 files, ~150 lines

```
backend/finance/app/
  ├── schemas/account.py (+5 lines) - Pydantic schema
  ├── models/account.py (+1 line) - ORM model
  └── services/account.py (+3 lines) - Business logic

tests/finance/
  └── test_account_service.py (+30 lines) - Unit tests
```

**Impacted Modules:**
- Finance Module (Account service) - PRIMARY
- Sales Module (Account Dashboard) - SECONDARY (read-only, backward compatible)

**Testing:**
- Unit tests: 3 new cases (happy path, edge cases, errors)
- Integration tests: Pass
- Coverage: 95%
```

### 3. Changes Summary

```markdown
## CHANGELOG Entry

### [v1.2.0] - 2026-05-07

#### Added
- Add `new_field` (optional string) to Account schema for custom metadata tracking
  - Enables Finance team to store Q2 reporting metadata
  - Nullable column, backward compatible with existing clients
  - Max length: 255 characters

#### Changed
- `AccountCreate` schema now includes `new_field: Optional[str]`
- `Account` ORM model includes `new_field` column

#### Testing
- Add 3 new unit tests for new_field validation
- All existing tests pass (regression check)
- Coverage: 95%

#### Notes
- ✅ Backward compatible (no breaking changes)
- ✅ No database migration required (nullable column)
- ✅ No API version bump needed
```

---

## ✅ DOCUMENTATION CHECKLIST

Before approving PHASE 7, verify:

**Code Comments:**
- [ ] Docstrings present on all public APIs
- [ ] Comments explain "why", not "what"
- [ ] No commented-out code
- [ ] Error conditions documented

**README / API Docs:**
- [ ] Usage examples provided
- [ ] Request/response schemas shown
- [ ] Error codes documented
- [ ] Backward compatibility mentioned
- [ ] Any breaking changes clearly marked

**CHANGELOG:**
- [ ] New features listed
- [ ] Bug fixes listed
- [ ] Breaking changes highlighted
- [ ] Migration instructions (if needed)

**Examples:**
- [ ] Code examples compile and run
- [ ] cURL/HTTP examples accurate
- [ ] Python examples match module imports

---

## 📊 DOCUMENTATION STANDARDS

**Docstring Format** (Google style):
```python
def method(arg1: str, arg2: int) -> bool:
    """One-line summary.
    
    Longer description explaining purpose, behavior, edge cases.
    
    Args:
        arg1: What this arg is
        arg2: What this arg is
    
    Returns:
        What this method returns
    
    Raises:
        ValueError: When this error occurs
        TypeError: When that error occurs
    
    Example:
        >>> result = method("test", 42)
        >>> print(result)
        True
    """
```

**Comment Style:**
```python
# WHY: Validate org exists to prevent FK constraint errors
org = self.db.query(Organization).filter_by(id=req.organization_id).first()

# GOOD: Explains intent
if not org:  # Organization must exist for account creation
    raise ValueError(...)

# BAD: Just restates code
if not org:  # Check if org is None
    raise ValueError(...)
```

---

## 🚨 DOCUMENTATION GATES

Documentation FAILS if:

- ❌ No docstrings on public APIs
- ❌ API examples don't work
- ❌ Backward compatibility not mentioned
- ❌ Error codes not documented
- ❌ README not updated for new features
- ❌ Comments are outdated or misleading

---

## 📞 ESCALATION

If documentation is incomplete:

1. **Identify gaps** (what's missing?)
2. **Generate missing docs** (examples, schemas, etc.)
3. **Review for accuracy** (do examples actually work?)
4. **Get approval** before proceeding to PHASE 8

---

## 🔗 NEXT STEP

→ Upon approval, proceed to **PHASE 8: PR + Ticket Comments** (`phases/PHASE-8-PR-MERGE.md`)
