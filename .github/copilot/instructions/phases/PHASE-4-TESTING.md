# PHASE 4: Unit Test Generation

**Tokens:** ~200-300 | **Duration:** 30-45 min | **Owner:** @api-dev OR Orchestrator  
**Gate:** ⏸️ WAIT_FOR_APPROVAL

---

## 📋 INPUT

- Generated code from PHASE 3
- Test conventions (pytest, fixtures, mocks)
- Task details (edge cases, error scenarios)

---

## 🎯 ACTIONS

1. **Generate unit tests** with happy path + error scenarios
2. **Include edge cases** and boundary conditions
3. **Mock external dependencies** (DB, S3, LLM)
4. **Ensure ≥95% code coverage**
5. **Test error handling paths** (not just happy path)

---

## ✅ REQUIRED CHECKLIST

Before generating tests, verify:

- [ ] Happy path test exists
- [ ] Edge cases identified (null, empty, max/min values, etc.)
- [ ] Error scenarios tested (validation errors, not found, conflicts)
- [ ] Mocks configured for external dependencies
- [ ] Fixtures use proper setup/teardown
- [ ] Coverage target ≥95%
- [ ] Test names are descriptive (test_create_account_with_valid_data)

---

## 📤 TEST OUTPUT (pytest Format)

```python
# file: tests/finance/test_account_service.py

import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException

from backend.finance.app.schemas.account import AccountCreate
from backend.finance.app.models.account import Account
from backend.finance.app.services.account import AccountService


@pytest.fixture
def db_mock():
    """Mock database session"""
    return MagicMock()


@pytest.fixture
def account_service(db_mock):
    """AccountService with mocked DB"""
    return AccountService(db_mock)


class TestAccountServiceCreate:
    """Test AccountService.create() method"""
    
    def test_create_account_happy_path(self, account_service, db_mock):
        """Test creating account with valid data"""
        # Setup
        req = AccountCreate(
            name="Acme Corp",
            organization_id=1,
            new_field="value"
        )
        
        # Mock query result
        mock_org = Mock()
        mock_org.id = 1
        db_mock.query.return_value.filter_by.return_value.first.return_value = mock_org
        
        # Execute
        result = account_service.create(req)
        
        # Assert
        assert result.name == "Acme Corp"
        assert result.organization_id == 1
        assert result.new_field == "value"
        db_mock.add.assert_called_once()
        db_mock.commit.assert_called_once()
    
    def test_create_account_new_field_optional(self, account_service, db_mock):
        """Edge case: new_field is optional, can be None"""
        # Setup
        req = AccountCreate(
            name="Minimal Corp",
            organization_id=1
        )
        
        mock_org = Mock()
        db_mock.query.return_value.filter_by.return_value.first.return_value = mock_org
        
        # Execute
        result = account_service.create(req)
        
        # Assert
        assert result.name == "Minimal Corp"
        assert result.new_field is None
    
    def test_create_account_new_field_max_length(self, account_service):
        """Edge case: new_field respects max length (255 chars)"""
        # Setup
        req = AccountCreate(
            name="Test Corp",
            organization_id=1,
            new_field="x" * 255  # Max allowed
        )
        
        # Should not raise validation error
        assert len(req.new_field) == 255
    
    def test_create_account_organization_not_found(self, account_service, db_mock):
        """Error case: organization_id doesn't exist"""
        # Setup
        req = AccountCreate(
            name="Acme Corp",
            organization_id=999  # Non-existent
        )
        
        db_mock.query.return_value.filter_by.return_value.first.return_value = None
        
        # Execute & Assert
        with pytest.raises(ValueError, match="Organization 999 not found"):
            account_service.create(req)
    
    def test_create_account_invalid_name_empty(self):
        """Error case: name cannot be empty"""
        with pytest.raises(ValueError):
            AccountCreate(
                name="",  # Empty name
                organization_id=1
            )
    
    def test_create_account_invalid_organization_id(self):
        """Error case: organization_id required"""
        with pytest.raises(ValueError):
            AccountCreate(
                name="Test Corp"
                # organization_id missing
            )


class TestAccountServiceUpdate:
    """Test AccountService.update() method - if applicable"""
    # ... similar test structure


class TestAccountServiceDelete:
    """Test AccountService.delete() method - if applicable"""
    # ... similar test structure
```

---

## 📊 TEST COVERAGE REQUIREMENTS

| Category | Coverage Target | Examples |
|----------|---|---|
| Happy Path | 60% | Create with valid data |
| Edge Cases | 25% | Null values, max/min, empty strings |
| Error Cases | 10% | Validation errors, not found, conflicts |
| Async/Retry | 5% | Timeout handling, retry logic |
| **Total** | **≥95%** | Coverage report via pytest |

---

## 🏗️ TEST STRUCTURE

**Always follow this pattern:**

```python
def test_feature_scenario(fixture1, fixture2):
    """One-line description of what test does"""
    
    # SETUP: Prepare data, mocks
    input_data = {...}
    mock_service.return_value = expected_result
    
    # EXECUTE: Run the code under test
    result = service.method(input_data)
    
    # ASSERT: Verify expectations
    assert result.field == expected_value
    mock_service.assert_called_once_with(expected_args)
```

---

## 🚨 TEST QUALITY GATES

Tests FAIL if:

- ❌ Coverage < 95%
- ❌ Missing happy path test
- ❌ No error scenario tests
- ❌ Mocks not configured properly (not isolated)
- ❌ Test names unclear (test_x is bad, test_create_account_with_valid_data is good)
- ❌ Sleep/wait in tests (use freezegun for time tests)
- ❌ Test depends on execution order (should be independent)

---

## 📞 ESCALATION

If test generation faces issues:

- **Coverage low:** Identify uncovered paths, add tests
- **Test fails:** Fix code in PHASE 3, regenerate tests
- **Mock complexity:** Simplify or split into integration tests
- **Flaky tests:** Use proper fixtures, avoid time-based assertions

---

## 🔗 NEXT STEP

→ Upon approval, proceed to **PHASE 5: Code Review** (`phases/PHASE-5-CODE-REVIEW.md`)
