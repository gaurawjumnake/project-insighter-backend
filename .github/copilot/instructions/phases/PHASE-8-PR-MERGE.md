# PHASE 8: PR + Ticket Comments

**Tokens:** ~100-150 | **Duration:** 15-25 min | **Owner:** Orchestrator  
**Gate:** ⏸️ READY_TO_MERGE (user decision)

---

## 📋 INPUT

- All previous phases completed and approved
- Generated code, tests, and documentation
- Ticket ID and description

---

## 🎯 ACTIONS

1. **Generate PR description** (changes, impact, testing summary)
2. **Create merge checklist** (final verification before merge)
3. **Post ticket update** (status, summary, next steps)
4. **Prepare release notes** (if applicable)

---

## 📤 PR DESCRIPTION OUTPUT

```markdown
# [PROJ-123] Add custom_field to Account schema

## Summary
Adds optional `custom_field` parameter to Account entity for tracking 
additional metadata. Required for Q2 reporting and customer segmentation.

## Changes
- ✅ Updated AccountCreate schema to include optional new_field
- ✅ Added new_field column to Account ORM model (nullable, max 255 chars)
- ✅ Updated AccountService.create() to handle new_field
- ✅ Added 3 unit tests (happy path, edge cases, error scenarios)
- ✅ Updated API documentation with usage examples
- ✅ Verified backward compatibility

## Impact

**Files Changed:** 4
```diff
backend/finance/app/schemas/account.py          +5 lines
backend/finance/app/models/account.py           +1 line
backend/finance/app/services/account.py         +3 lines
tests/finance/test_account_service.py          +30 lines
```

**Risk Level:** 🟢 LOW
- New field is optional → backward compatible
- No breaking API changes
- No database migration needed
- Nullable column safely added

**Modules Affected:**
- Finance Module (Account service) - PRIMARY
- Sales Module (Account Dashboard) - Secondary (read-only)

## Testing

- ✅ Unit tests: 3 new cases (happy path, edge cases, errors)
- ✅ Integration tests: All pass
- ✅ Coverage: 95%
- ✅ Regression: Existing tests all pass
- ✅ Performance: No N+1 queries, no new indexes needed

**Test Coverage Report:**
```
tests/finance/test_account_service.py ... PASSED [3 new]
tests/finance/test_account_api.py ........ PASSED
Overall Coverage: 95%
```

## Backward Compatibility

✅ **Fully backward compatible**
- `new_field` is optional (nullable in DB)
- Existing API clients unaffected
- No schema version bump needed
- Existing requests continue to work

## API Documentation

**New Request Example:**
```bash
POST /api/v1/accounts
{
  "name": "Acme Corp",
  "organization_id": 1,
  "new_field": "Q2 metadata"
}

# Response
{
  "id": 42,
  "name": "Acme Corp",
  "new_field": "Q2 metadata",
  "created_at": "2026-05-07T10:30:00Z",
  ...
}
```

**Error Handling:**
- `400 Bad Request` — Missing required fields
- `404 Not Found` — Organization doesn't exist
- `422 Unprocessable Entity` — Validation failed (new_field > 255 chars)

## Deployment Notes

- ✅ No database migration (nullable column added safely)
- ✅ No environment variables needed
- ✅ No external dependencies added
- ✅ No feature flags needed

**Deploy Steps:**
1. Merge to main
2. Run tests in CI/CD (should all pass)
3. Deploy to staging for final testing
4. Deploy to production

## Review Checklist

- [x] Code follows repo conventions (PATTERNS.md)
- [x] All tests pass (≥95% coverage)
- [x] No hardcoded secrets or config
- [x] Error handling complete
- [x] Docstrings and comments present
- [x] API documentation updated
- [x] Backward compatibility verified
- [x] Performance impact assessed (none)

## Related Issues

- Blocked by: None
- Blocks: PROJ-124 (Sales Dashboard enhancement)
- Relates to: PROJ-122 (Similar schema change)

## Reviewers
- @tech-lead (code review)
- @qa-engineer (final testing)

---

## 📋 MERGE CHECKLIST (Before Clicking "Merge")

**Code Quality:**
- [ ] All tests pass (locally and CI/CD)
- [ ] Coverage ≥95%
- [ ] No lint errors
- [ ] Type hints present

**Safety:**
- [ ] No hardcoded secrets
- [ ] No commented-out code
- [ ] Error handling correct
- [ ] SQL injection risk assessed (none)

**Backward Compatibility:**
- [ ] No breaking API changes
- [ ] No database migration required
- [ ] Existing clients unaffected
- [ ] Rollback plan (if needed)

**Documentation:**
- [ ] README updated
- [ ] API docs updated
- [ ] Comments and docstrings present
- [ ] CHANGELOG updated

**Deployment:**
- [ ] No new environment variables
- [ ] No new dependencies
- [ ] No feature flags needed
- [ ] Deployment instructions clear

---

## 📞 TICKET UPDATE COMMENT

```markdown
## Status Update: READY_FOR_REVIEW

**Ticket:** PROJ-123  
**Status:** ✅ Code complete, ready for review  
**Last Updated:** 2026-05-07 14:30 UTC

### Summary
Implementation of custom_field addition to Account schema is complete.

### Deliverables
- ✅ Code generated and tested
- ✅ Unit tests: 3 new cases (happy path, edge cases, errors)
- ✅ Code reviewed: No blocking issues
- ✅ Documentation updated
- ✅ PR ready: #789

### Quality Metrics
- Test Coverage: 95%
- Risk Level: LOW
- Breaking Changes: None
- Backward Compatibility: ✅ Yes

### Files Changed
- backend/finance/app/schemas/account.py (+5)
- backend/finance/app/models/account.py (+1)
- backend/finance/app/services/account.py (+3)
- tests/finance/test_account_service.py (+30)

### Next Steps
1. Code review by @tech-lead
2. QA testing in staging
3. Merge to main
4. Deploy to production

### Artifacts
- PR: #789
- Test Report: [link]
- Coverage Report: [link]
- Documentation: [link to API docs]

**Questions?** Comment here or reach out to [developer name]
```

---

## 🎉 RELEASE NOTES (If Applicable)

```markdown
## Release Notes - v1.2.0

### New Features
- [#789] Add custom metadata tracking to Account entity
  - New optional `new_field` parameter for custom metadata
  - Enables Q2 reporting and customer segmentation
  - Backward compatible with existing integrations

### Bug Fixes
- None in this release

### Improvements
- Improved Account schema validation
- Enhanced error messages for invalid inputs

### Breaking Changes
- None

### Migration Guide
No database migration required. The new column is nullable and 
created automatically on deployment.

**Backward Compatibility:** ✅ Fully backward compatible

### Contributors
- @developer-name (implementation)
- @tech-lead (review)

### Release Date
2026-05-07
```

---

## ✅ FINAL APPROVAL CHECKLIST

Before marking as **READY_TO_MERGE**:

- [ ] All phases approved (1-7)
- [ ] All tests passing (CI/CD green)
- [ ] PR template filled
- [ ] Code review approved
- [ ] No merge conflicts
- [ ] Deployment plan clear
- [ ] No blocking issues

---

## 🚨 MERGE BLOCKERS

**Do NOT merge if:**

- ❌ Tests failing (coverage < 95%)
- ❌ Lint errors present
- ❌ Code review has blocking comments
- ❌ Breaking changes not documented
- ❌ Risk level not assessed
- ❌ Security review not done

---

## 📞 ESCALATION

If there are merge blockers:

1. **Identify blocker** (test failure? code review issue?)
2. **Return to appropriate phase** (PHASE 3, 4, 5, or 7)
3. **Fix issue** (regenerate code, retests, etc.)
4. **Re-review** (all relevant phases)
5. **Return to PHASE 8** for final approval

---

## 🔁 POST-MERGE TASKS (Not Phase Responsibility)

These are handled by DevOps/SRE after merge:

- Merge to main branch
- Trigger CI/CD pipeline
- Run integration tests
- Deploy to staging
- Smoke test in staging
- Deploy to production
- Monitor for errors
- Notify stakeholders

---

## 🎯 SUCCESS CRITERIA

Ticket moves to **CLOSED** when:

✅ PR merged to main  
✅ Code deployed to production  
✅ No critical bugs reported  
✅ Acceptance criteria met  
✅ Stakeholders notified  

---

## 📊 WORKFLOW COMPLETE

```
PHASE 1: Context + Impact Analysis ✅
PHASE 2: Task Breakdown ✅
PHASE 3: Code Generation ✅
PHASE 4: Unit Testing ✅
PHASE 5: Code Review ✅
PHASE 6: Bug Triage (if applicable) ✅
PHASE 7: Documentation ✅
PHASE 8: PR + Ticket Comments ✅
───────────────────────────────────
READY_TO_MERGE
```

---

## 🔗 RELATED DOCUMENTATION

- [workflow-orchestrator.md](../workflow-orchestrator.md) — Overview of all phases
- [requirement-analysis.md](../requirement-analysis.md) — How to submit requirements
- [AGENTS.md](../../agents/AGENTS.md) — Which agent handles which phase
