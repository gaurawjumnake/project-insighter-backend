# PHASE 5: Code Review (AI Self-Review)

**Tokens:** ~100-150 | **Duration:** 20-30 min | **Owner:** Orchestrator  
**Gate:** ⏸️ WAIT_FOR_APPROVAL

---

## 📋 INPUT

- Generated code from PHASE 3
- Generated tests from PHASE 4
- Codebase patterns (PATTERNS.md)

---

## 🎯 ACTIONS

1. **Validate logic correctness** (does code do what it should?)
2. **Check for security vulnerabilities** (SQL injection, secrets, auth)
3. **Identify performance risks** (N+1 queries, inefficient loops)
4. **Verify test coverage ≥95%** (all code paths tested?)
5. **Check naming conventions** (match codebase style)
6. **Validate error handling** (all failure modes covered?)

---

## 📤 CODE REVIEW OUTPUT (YAML Format)

```yaml
phase: 5_code_review
ticket_id: "PROJ-123"

review_checklist:
  logic_correctness: ✅ PASS
    - Account model correctly inherits from Base
    - Service layer properly validates input
    - Pydantic schema matches ORM model
    - Dependencies tracked correctly
  
  security: ✅ PASS
    - No SQL injection (parameterized queries via SQLAlchemy)
    - No hardcoded secrets (config via environment variables)
    - Input validation present (Pydantic schemas)
    - No exposed internal state in error messages
  
  performance: ⚠️ WARNING
    - issue: "N+1 query risk in AccountService.list()"
    - severity: medium
    - location: "backend/finance/app/services/account.py:45"
    - suggestion: "Add relationship eager loading with joinedload()"
    - priority: "fix before merge"
  
  test_coverage: ✅ PASS (95%)
    - Happy path tests: ✅
    - Edge case tests: ✅
    - Error scenario tests: ✅
    - Coverage report: tests/coverage.html
  
  naming_conventions: ✅ PASS
    - CamelCase for classes: ✅
    - snake_case for functions: ✅
    - Docstrings present: ✅
    - Comments clear: ✅
  
  error_handling: ✅ PASS
    - Specific exceptions (not bare except:): ✅
    - HTTP error codes mapped correctly: ✅
    - Validation errors caught: ✅
    - Null checks present: ✅

code_quality_metrics:
  lines_of_code: 147
  cyclomatic_complexity: 3  # Low
  type_hint_coverage: 100%
  docstring_coverage: 100%

files_reviewed:
  - backend/finance/app/schemas/account.py ✅
  - backend/finance/app/models/account.py ✅
  - backend/finance/app/services/account.py ✅
  - tests/finance/test_account_service.py ✅

issues_found: 1  # Non-blocking warning
blocking_issues: 0  # Would prevent merge
suggestions:
  - "Consider adding relationship caching for future optimization"

overall_risk: low
ready_to_merge: true

reviewer_notes: >
  Code is well-structured and follows codebase patterns.
  Single performance warning is not critical but should be addressed
  in future optimization pass. No blocking issues found.
```

---

## ✅ REVIEW CHECKLIST

Before approving PHASE 5, verify:

**Logic & Correctness:**
- [ ] Code implements the requirement correctly
- [ ] Business logic is sound
- [ ] Edge cases handled
- [ ] Null checks present where needed

**Security:**
- [ ] No SQL injection risks (parameterized queries)
- [ ] No hardcoded secrets or credentials
- [ ] Input validation present
- [ ] Error messages don't expose internals

**Performance:**
- [ ] No N+1 queries (for database operations)
- [ ] No inefficient loops or algorithms
- [ ] Database queries optimized (eager loading where needed)
- [ ] No memory leaks (proper cleanup)

**Testing:**
- [ ] Coverage ≥95%
- [ ] Happy path test exists
- [ ] Error cases tested
- [ ] Edge cases covered
- [ ] Mocks isolated from external dependencies

**Code Style:**
- [ ] Follows naming conventions (PATTERNS.md)
- [ ] Docstrings present and clear
- [ ] Comments explain "why", not "what"
- [ ] No commented-out code

**Error Handling:**
- [ ] No bare except: blocks
- [ ] Specific exception types caught
- [ ] HTTP error codes correct (400, 404, 422, 500, etc.)
- [ ] Error messages helpful

---

## 🚨 BLOCKING ISSUES

Review FAILS if any of these are present:

- ❌ Unhandled exception path
- ❌ SQL injection vulnerability
- ❌ Hardcoded secrets
- ❌ Test coverage < 90%
- ❌ Type hints missing on public APIs
- ❌ Bare except: blocks

---

## ⚠️ NON-BLOCKING WARNINGS

Review PASSES but flag these for future work:

- ⚠️ Performance optimization opportunity (fix later)
- ⚠️ Code duplication (refactor in future PR)
- ⚠️ Missing logging (add if important)
- ⚠️ Could use caching (optimize if needed)

---

## 📞 ESCALATION

If review finds blocking issues:

1. **Document the issue** (what, where, why)
2. **Suggest fix** (specific code change)
3. **Return to PHASE 3** (code regeneration)
4. **Re-run PHASE 4** (retests)
5. **Re-review in PHASE 5** (verification)

---

## 🔗 NEXT STEP

→ Upon approval, proceed to **PHASE 7: Documentation** (`phases/PHASE-7-DOCUMENTATION.md`)

→ If BUG mode, instead go to **PHASE 6: Bug Triage** (`phases/PHASE-6-BUG-TRIAGE.md`)
