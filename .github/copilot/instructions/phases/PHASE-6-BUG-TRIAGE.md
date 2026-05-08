# PHASE 6: Bug Triage (BUG MODE ONLY)

**Tokens:** ~150-200 | **Duration:** 20-30 min | **Owner:** Orchestrator  
**Gate:** ⏸️ WAIT_FOR_APPROVAL

---

## 📋 INPUT

- Bug description from ticket
- Impacted files from PHASE 1 (Context + Impact Analysis)
- Stacktrace or reproduction steps (if available)

---

## 🎯 ACTIONS

1. **Classify severity** (low / medium / high / critical)
2. **Identify root cause** (what went wrong, where in code?)
3. **Assess regression risk** (does fix introduce new problems?)
4. **Determine fix strategy** (minimal change vs refactor)
5. **Plan verification** (how to test the fix)

---

## 📤 BUG TRIAGE OUTPUT (YAML Format)

```yaml
phase: 6_bug_triage
ticket_id: "BUG-456"

bug_title: "AccountService.create() fails with null organization_id"
bug_description: |
  When creating an account with organization_id=null, the service
  crashes instead of returning a validation error.

root_cause:
  file: "backend/finance/app/services/account.py"
  line: 42
  function: "AccountService.create()"
  issue: "Missing null check before accessing organization_id"
  
  problematic_code: |
    org_id = req.organization_id  # No validation
    # ... later in code ...
    org = self.db.query(Organization).filter_by(id=org_id).first()
    # If org_id is None, query returns None, causes error downstream
  
  expected_behavior: "Should validate organization_id before using it"

severity_classification:
  level: medium  # low | medium | high | critical
  
  rationale: >
    Affects account creation flow, but data validation in Pydantic schema
    should have caught this. Impact limited to invalid input scenarios.
  
  impact_scope:
    - API endpoint: POST /api/v1/accounts
    - Module: Finance - Account Service
    - Users affected: Low (only happens with malformed requests)
  
  data_loss_risk: low  # No data loss, just validation failure

affected_modules:
  - Finance Module (Account service) - PRIMARY
  - API validation (should catch earlier) - SECONDARY

fix_strategy: minimal  # minimal | targeted | refactor | redesign
  
  approach: >
    Add validation in two layers:
    1. Pydantic schema: Mark organization_id as required (non-optional)
    2. Service layer: Add explicit null check before query
  
  changes_required:
    - backend/finance/app/schemas/account.py: Add required validation
    - backend/finance/app/services/account.py: Add null check
    - tests/finance/test_account_service.py: Add regression test
  
  alternative_approaches:
    - Add database constraint (NOT NULL) - requires migration
    - Add upstream validation in API route - duplicates schema validation

regression_risk:
  level: low
  
  rationale: >
    Validation is backward compatible. Requests that were failing
    will now fail with better error message. No breaking changes.
  
  mitigation: >
    - Add regression test to prevent this exact bug
    - Verify existing account creation tests still pass
    - Check Sales module (uses same Account model) not affected

verification_plan:
  unit_tests:
    - Test with null organization_id (should raise ValueError)
    - Test with valid organization_id (should succeed)
    - Test with non-existent organization_id (should raise NotFound)
  
  integration_tests:
    - POST /api/v1/accounts with null org_id (should return 422)
    - POST /api/v1/accounts with valid org_id (should return 201)
  
  manual_tests:
    - Reproduce original bug (confirm fix)
    - Verify error message is clear

priority: medium
  rationale: "Not production-critical but should fix in next sprint"

related_issues:
  - PROJ-122: Similar null check missing in ProjectService
  - PROJ-124: General validation audit needed
```

---

## ✅ BUG TRIAGE CHECKLIST

Before approving PHASE 6, verify:

- [ ] Root cause identified (specific file, line, function)
- [ ] Severity classified correctly
- [ ] Impact scope clearly defined
- [ ] Fix strategy is sound (minimal, not over-engineering)
- [ ] Regression risk assessed
- [ ] Verification plan clear (tests to run)
- [ ] No scope creep (fixing related bugs in separate tickets)

---

## 🔍 ROOT CAUSE ANALYSIS PATTERN

**Always investigate these areas:**

1. **Input validation** — Did we validate the input?
2. **Null checks** — Did we handle null/None values?
3. **Error handling** — Did we catch exceptions?
4. **Dependencies** — Did we call external service correctly?
5. **State** — Is there shared state causing race conditions?
6. **Async** — Are there async race conditions?
7. **Configuration** — Is it a config issue (missing env var)?

---

## 📊 SEVERITY MAPPING

| Level | Criteria | Action |
|-------|----------|--------|
| **CRITICAL** | Production down, data loss, security | HOTFIX NOW |
| **HIGH** | Major feature broken, P1 customer impact | Fix next day |
| **MEDIUM** | Feature partially broken, edge cases | Fix this sprint |
| **LOW** | Minor inconvenience, workaround exists | Backlog |

---

## 🚨 ESCALATION

If any of these apply, **escalate bug triage:**

- Severity = CRITICAL
- Root cause unclear (insufficient info)
- Fix requires major refactoring
- Bug affects multiple modules
- Data loss or security vulnerability

---

## 🔗 NEXT STEPS

→ Upon approval, proceed to:

- **For FEATURE/REFACTOR mode:** Go to **PHASE 7: Documentation** (`phases/PHASE-7-DOCUMENTATION.md`)
- **For BUG mode:** Go to **PHASE 3: Code Generation** (`phases/PHASE-3-CODE-GENERATION.md`) to apply fix
