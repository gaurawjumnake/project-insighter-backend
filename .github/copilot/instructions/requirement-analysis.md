# Requirement Analysis — Pre-Phase 1 Intake

**Version:** 1.0 | **Date:** 2026-05-07  
**Purpose:** Structured intake & classification of incoming requests before PHASE 1 (Context + Impact)

---

## 📋 INTAKE TEMPLATE

Use this template when submitting a request to the Orchestrator:

```yaml
## REQUEST METADATA
ticket_id: "PROJ-123"  # Jira key (optional)
submitted_by: "Engineer Name"
submitted_date: "2026-05-07"
priority: "p2"  # p0 (urgent) | p1 (high) | p2 (medium) | p3 (low)
urgency: "normal"  # normal | hotfix | planning

## REQUIREMENT DESCRIPTION
title: "Add custom_field to Account schema"
type: "feature"  # feature | bug | refactor (auto-detect if unclear)
description: |
  The Finance team needs to track additional metadata on Account entities.
  This is required for Q2 reporting and customer segmentation.

## CONTEXT & BACKGROUND
related_modules:
  - Finance Module (primary)
  - Sales Module (potential impact for dashboards)

related_documents:
  - SOW document references
  - Confluence page link
  - Email thread

known_constraints:
  - Must be backward compatible
  - No database migration (use nullable column)
  - Must support existing API clients

## OPTIONAL: GRAPHIFY HINTS
specific_graph_query: "How does Account relate to AccountDashboard?"
file_references:
  - backend/finance/app/models/account.py
  - backend/finance/app/schemas/account.py

## ACCEPTANCE CRITERIA
must_have:
  - New field appears in API response
  - Existing code continues to work (no breaking changes)
  - Tests verify new field behavior

nice_to_have:
  - Update documentation with usage example
  - Add to frontend form (lower priority)

## LINKED ITEMS
blocks: []  # What does this unblock?
blocked_by: []  # Does this depend on something else?
related_tickets: ["PROJ-122", "PROJ-124"]
```

---

## 🔍 CLASSIFICATION RULES

### FEATURE: New Behavior / Capability
✅ **Indicators:**
- New API endpoint (`POST /api/v1/...`)
- New field on existing model (with new logic)
- New insight type or document processor
- New AI crew or tool
- Extends module to handle new use case

❌ **NOT a feature:**
- Bug fix (behavior is already correct, just broken)
- Performance optimization (behavior unchanged)
- Code cleanup (purely refactoring)

**Example:**
```
User: "Add custom_field to Account for metadata tracking"
→ NEW field with new storage/retrieval logic = FEATURE
→ Mode: FEATURE (phases 1→2→3→4→5→7→8)
```

---

### BUG: Incorrect Behavior / Unexpected Error
✅ **Indicators:**
- API returns wrong status code
- Data is corrupted or missing
- Validation fails unexpectedly
- Edge case not handled (null, empty, large value)
- Performance degradation
- Security vulnerability

❌ **NOT a bug:**
- Missing feature (file a feature request)
- Documentation unclear (documentation fix)
- API design could be better (refactoring request)

**Example:**
```
User: "AccountService.create() fails with null organization_id"
→ Bug in validation logic = BUG
→ Mode: BUG (phases 1→6→3→4→5→7→8)
```

---

### REFACTOR: Code Quality / Structure Improvement
✅ **Indicators:**
- Rename variables/functions for clarity
- Reorganize module structure
- Optimize N+1 queries (behavior preserved)
- Extract duplicated code
- Improve type hints / docstrings
- Simplify complex function

⚠️ **CONSTRAINT:** Zero behavior change

❌ **NOT a refactor:**
- Adding new logic (that's a feature)
- Fixing incorrect behavior (that's a bug)
- Changing API contract (that's a breaking change)

**Example:**
```
User: "Refactor Finance module for N+1 optimization"
→ Performance improvement, same behavior = REFACTOR
→ Mode: REFACTOR (phases 1→2→3→4 [regression]→5→7→8)
```

---

## 🎯 AUTO-CLASSIFICATION ALGORITHM

If type is unclear, apply these rules:

```
1. Does it fix a bug?
   → TYPE = BUG
   
2. Does it change behavior / add capability?
   → TYPE = FEATURE
   
3. Does it reorganize/optimize WITHOUT changing behavior?
   → TYPE = REFACTOR
   
4. Still unclear?
   → Ask user: "Is this adding NEW capability or fixing BROKEN behavior?"
```

---

## 🔗 DEPENDENCY MAPPING

**Before PHASE 1, identify dependencies:**

```yaml
dependencies:
  blocks: []  # This work unblocks what?
  blocked_by: []  # Does this depend on something?
  
# Example:
blocks:
  - "PROJ-124: Add risk_score field to Project"  # Depends on custom_field
  - "SALES-45: Update dashboard to show custom_field"

blocked_by:
  - "PROJ-122: Create Organization model (must exist first)"
```

**Impact:**
- If blocked → move to planning queue, add blocker link
- If blocks others → flag as critical path item
- If blocked_by not started → can't begin Phase 1

---

## 📊 SCOPE ESTIMATION GUIDE

Use this to pre-estimate Phase 2 tasks:

| Scope | Est. Time | Task Count | Example |
|-------|-----------|-----------|---------|
| **xs** | <15 min | 1-2 | "Add field to schema + model" |
| **s** | 15-45 min | 2-4 | "Simple API endpoint + tests" |
| **m** | 45min-2h | 4-8 | "Full CRUD endpoint + tests + docs" |
| **l** | 2-6h | 8-15 | "Cross-module feature + integration tests" |
| **xl** | 6+ hours | 15+ | "Major refactor or new module" |

**Estimation:**
- Count files to modify
- Count new test cases needed
- Count doc sections to update
- Use table above

---

## 🚨 RED FLAGS / ESCALATION RULES

**Escalate to senior engineer / PM if:**

| Flag | Action |
|------|--------|
| Unknown scope ("design TBD") | **STOP**: Get requirements before Phase 1 |
| Cross-team impact (Finance + Sales + AI) | **ALERT**: Requires coordination, add to planning |
| Potential breaking change | **STOP**: Review API contract first |
| Security-related ("fix vulnerability") | **URGENT**: Route to security team, P0 priority |
| Database migration required | **STOP**: Migration strategy needed before code |
| Performance-critical ("optimize for speed") | **ALERT**: Add performance acceptance criteria |
| No acceptance criteria defined | **STOP**: Define pass/fail before Phase 2 |

---

## ✅ REQUIREMENT VALIDATION CHECKLIST

**Before approving PHASE 1, verify:**

- ✅ Request is clear and unambiguous
- ✅ Type is correctly classified (feature / bug / refactor)
- ✅ Priority and urgency are reasonable
- ✅ At least 1 acceptance criterion defined
- ✅ No "TBD" or "to be determined" in description
- ✅ Known constraints are documented
- ✅ Blocked-by dependencies are resolved
- ✅ Graphify hints provided (if available)

**If ANY fail → Request more info before Phase 1**

---

## 📝 REQUEST EXAMPLES

### Example 1: Feature Request

```yaml
ticket_id: "PROJ-123"
title: "Add custom_field to Account schema"
type: "feature"
description: |
  Finance team needs to store custom metadata on Accounts
  for Q2 reporting. Field should be optional, searchable,
  and visible in account list API.

related_modules:
  - Finance Module (primary)
  - Sales Module (dashboard might show field)

must_have:
  - Field appears in GET /api/v1/accounts/{id}
  - Field is optional (backward compatible)
  - Can filter accounts by custom_field

nice_to_have:
  - Search/sort by custom_field
  - Add to account dashboard

blocks: ["PROJ-124: Q2 reporting features"]
priority: "p2"
```

**Classification → FEATURE**  
**Mode → Feature (phases 1→2→3→4→5→7→8)**

---

### Example 2: Bug Report

```yaml
ticket_id: "BUG-456"
title: "AccountService.create() fails with null organization_id"
type: "bug"
description: |
  When AccountCreate request has organization_id=null,
  the service crashes with NoForeignKeyError instead of
  returning 400 Bad Request. This breaks the API contract.

related_modules:
  - Finance Module (Account service)

repro_steps:
  1. POST /api/v1/accounts with {"name": "Test", "organization_id": null}
  2. Expected: 400 Bad Request
  3. Actual: 500 Internal Server Error

must_have:
  - Return 400 Bad Request on null organization_id
  - Response includes validation error message
  - Unit test prevents regression

priority: "p1"  # Breaking the API
```

**Classification → BUG**  
**Mode → Bug (phases 1→6→3→4→5→7→8)**

---

### Example 3: Refactor Request

```yaml
ticket_id: "REFACTOR-78"
title: "Optimize Finance queries for N+1 problem"
type: "refactor"
description: |
  Finance list endpoints currently load 1 query per account
  for relationships (projects, documents, revenue).
  Should use joinedload to fetch all in 1-2 queries.
  Zero behavior change — same data, faster response.

related_modules:
  - Finance Module (all list endpoints)

known_constraints:
  - NO behavior change (same data returned)
  - Existing tests MUST still pass
  - Backward compatible API responses

acceptance_criteria:
  - Query count reduced: 1 main + N per account → 1-2 total
  - Response time improved by 50%+
  - All tests pass (regression suite)

blocks: ["PERF-90: Response time SLA < 200ms"]
priority: "p3"
```

**Classification → REFACTOR**  
**Mode → Refactor (phases 1→2→3→4 [regression]→5→7→8)**

---

## 🔄 INTAKE WORKFLOW

**Step 1: User submits request**
```
Email / Slack / Jira ticket
→ Include: title, description, type, priority
```

**Step 2: Orchestrator validates intake**
```
✅ Can auto-detect type?
✅ All required fields present?
✅ Red flags checked?
→ If missing: ASK FOR MORE INFO
→ If red flag: ESCALATE
```

**Step 3: Classify and route**
```
Type = feature / bug / refactor?
Priority = p0 / p1 / p2 / p3?
→ Route to correct mode
→ Schedule Phase 1
```

**Step 4: Proceed to Phase 1**
```
Fetch Graphify context
Run impact analysis
Output structured PHASE 1 report
→ WAIT_FOR_APPROVAL
```

---

## 📞 ASKING FOR CLARIFICATION

**If requirement is unclear, use this template:**

```
❓ **CLARIFICATION NEEDED**

Topic: {field that's unclear}

Question: {specific question}

Why needed: {why we need this info}

Please provide:
- {specific detail}
- {specific detail}

Example: {example of what we expect}
```

**Example:**
```
❓ **CLARIFICATION NEEDED**

Topic: Acceptance Criteria

Question: "What does 'searchable by custom_field' mean?"

Why needed: Affects API design (query param vs full-text search)

Please provide:
- Exact filter API endpoint format
- Search on exact match or partial?
- Case-sensitive or case-insensitive?

Example: "GET /api/v1/accounts?custom_field=value1" or "GET /api/v1/accounts/search?q=value1"?
```

---

## 🔗 RELATED DOCS

- [workflow-orchestrator.md](workflow-orchestrator.md) — SDLC phase definitions
- [PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md) — Project context
- [PATTERNS.md](PATTERNS.md) — Codebase conventions (helps classify scope)
