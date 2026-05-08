# Workflow Orchestrator — Gated SDLC Entry Point

**Version:** 1.0 | **Date:** 2026-05-07  
**Purpose:** Route incoming tickets → requirement analysis → determine mode → dispatch to phases with approval gates

> **✨ NEW:** For token-optimized phase definitions, see `instructions/phases/` directory.  
> Each phase now has its own focused file (100-200 lines) instead of one large orchestrator.  
> **Quick Links:** [PHASE-1](phases/PHASE-1-CONTEXT-IMPACT.md) | [PHASE-2](phases/PHASE-2-TASK-BREAKDOWN.md) | [PHASE-3](phases/PHASE-3-CODE-GENERATION.md) | [PHASE-4](phases/PHASE-4-TESTING.md) | [PHASE-5](phases/PHASE-5-CODE-REVIEW.md) | [PHASE-6](phases/PHASE-6-BUG-TRIAGE.md) | [PHASE-7](phases/PHASE-7-DOCUMENTATION.md) | [PHASE-8](phases/PHASE-8-PR-MERGE.md)

---

## 🚀 QUICK START

### For Users (Engineers, PMs, QA)
1. **Submit request** with:
   - Ticket ID / requirement / bug description
   - Optional: context, urgency, related files
2. **Orchestrator runs PHASE 1** (Context + Impact)
3. **Review output** → Approve / Reject
4. **Orchestrator determines mode** (feature / bug / refactor)
5. **Proceed through phases** (each with approval gate)

### For Copilot Agents
- **@api-dev**: Owner of PHASE 3 (Code Gen), PHASE 4 (Tests), PHASE 7 (Docs) for API changes
- **@ai-arch**: Owner of PHASE 3 (Code Gen), PHASE 4 (Tests) for AI/Crew changes
- **Orchestrator**: Owner of PHASE 1, 2, 5, 6, 8

---

## 🎯 ORCHESTRATOR RESPONSIBILITIES

### 1. Parse Incoming Request
```yaml
expected_format:
  ticket_id: "PROJ-123"  # Optional Jira key
  type: "feature|bug|refactor"  # or auto-detect
  description: "User story or bug report"
  context: "Additional details, file references, priority"
  graphify_query: "Optional - specific graph context"
```

### 2. Fetch Graphify Context (MANDATORY for PHASE 1)

**Before running PHASE 1, load:**

1. **Human-Readable Report:**
   - Location: `graphify-out/GRAPH_REPORT.md`
   - Contains: God Nodes (5 total), Communities (42 total), Metrics (917 nodes)
   - Use for: Quick overview of architecture, god nodes, communities

2. **Raw Graph Data:**
   - Location: `graphify-out/graph.json`
   - Contains: nodes[], edges[], communities[] with relationships
   - Use for: Querying specific impacted files, tracing dependencies

3. **Module-Specific Cache (if needed):**
   - Location: `graphify-out/cache/<module_hash>.json`
   - Contains: Individual module analysis
   - Use for: Deep dive on specific modules

**Graphify provides:**
- Related files & modules (via graph.json node relationships)
- Dependency graph (edges between nodes)
- God nodes (5 critical abstractions: Account, Project, Logger, RevenueMaster, LlamaCloudDocumentParser)
- Communities (42 cohesive subsystems: Finance Services, Sales Services, Doc Processing, etc.)
- Risk metrics (god node involvement, change propagation)

**If graphify-out/ is missing or stale:**
```bash
uv run graphify analyze
# Regenerates: GRAPH_REPORT.md, graph.json, cache/, metrics
# Duration: 1-2 minutes
```

### 3. Run PHASE 1: Context + Impact Analysis
See: [PHASE 1](#phase-1-context--impact-analysis)

### 4. Classify Request Type
```yaml
classification:
  # FEATURE: New API endpoint, new insight type, new processor
  feature:
    characteristics:
      - Adds new behavior
      - Extends existing modules
      - May span multiple services
    mode_trigger: "feature"
  
  # BUG: Fix incorrect behavior, handle edge case
  bug:
    characteristics:
      - Incorrect logic or data
      - Error not caught
      - Performance/security issue
    mode_trigger: "bug"
  
  # REFACTOR: Improve existing code, no behavior change
  refactor:
    characteristics:
      - Rename, reorganize, optimize
      - Must include regression tests
      - Zero behavior change
    mode_trigger: "refactor"
```

### 5. Determine Workflow Mode
Routes to specialized phase sequences:

| Mode | Phase Sequence | Use Case |
|------|---|---|
| **FEATURE** | 1 → 2 → 3 → 4 → 5 → 7 → 8 | New API, new AI crew, new processor |
| **BUG** | 1 → 6 → 3 → 4 → 5 → 7 → 8 | Fix existing behavior, trace root cause |
| **REFACTOR** | 1 → 2 → 3 → 4 (regression) → 5 → 7 → 8 | Improve code quality, optimize |

### 6. Output Phase Gates
Each phase produces structured YAML output → requires explicit approval before proceeding

---

## 🔁 WORKFLOW MODES

### Mode 1: FEATURE (Full Workflow)

```yaml
mode: feature
phases_sequence: [1, 2, 3, 4, 5, 7, 8]

phase_1:
  action: "Analyze impact, identify services, dependencies"
  owner: "Orchestrator + Graphify"
  gate: "WAIT_FOR_APPROVAL"

phase_2:
  action: "Break into atomic dev tasks"
  owner: "Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_3:
  action: "Generate/modify code (API or AI)"
  owner: "@api-dev OR @ai-arch"
  gate: "WAIT_FOR_APPROVAL"

phase_4:
  action: "Generate unit tests + edge cases"
  owner: "@api-dev OR Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_5:
  action: "Self-review: logic, security, performance"
  owner: "Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_7:
  action: "Update docs, inline comments, README"
  owner: "@api-dev OR Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_8:
  action: "Generate PR + ticket comments"
  owner: "Orchestrator"
  gate: "READY_TO_MERGE (user decision)"
```

### Mode 2: BUG (Root Cause → Fix → Test)

```yaml
mode: bug
phases_sequence: [1, 6, 3, 4, 5, 7, 8]

phase_1:
  action: "Analyze impact, identify affected modules"
  owner: "Orchestrator + Graphify"
  gate: "WAIT_FOR_APPROVAL"

phase_6:
  action: "Classify bug: root cause, severity, fix strategy"
  owner: "Orchestrator"
  output_format: "See PHASE 6 below"
  gate: "WAIT_FOR_APPROVAL"

phase_3:
  action: "Apply fix (minimal change)"
  owner: "@api-dev OR @ai-arch"
  gate: "WAIT_FOR_APPROVAL"

phase_4:
  action: "Unit test for bug + edge cases (prevent regression)"
  owner: "@api-dev OR Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_5:
  action: "Verify fix doesn't introduce new issues"
  owner: "Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_7:
  action: "Document fix, update tests"
  owner: "Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_8:
  action: "Generate PR + ticket comments"
  owner: "Orchestrator"
  gate: "READY_TO_MERGE"
```

### Mode 3: REFACTOR (Quality Improvement)

```yaml
mode: refactor
phases_sequence: [1, 2, 3, 4, 5, 7, 8]

phase_1:
  action: "Identify scope, current patterns, risk"
  owner: "Orchestrator + Graphify"
  constraint: "Zero behavior change"
  gate: "WAIT_FOR_APPROVAL"

phase_2:
  action: "Break into reorg/rename/optimize tasks"
  owner: "Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_3:
  action: "Apply refactoring (rename, reorganize, optimize)"
  owner: "@api-dev OR Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_4:
  action: "Generate REGRESSION tests (verify behavior preserved)"
  owner: "@api-dev"
  critical: "MUST pass all old tests + new regression suite"
  gate: "WAIT_FOR_APPROVAL"

phase_5:
  action: "Verify no logic change, only improvement"
  owner: "Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_7:
  action: "Update docs (rationale for refactor)"
  owner: "Orchestrator"
  gate: "WAIT_FOR_APPROVAL"

phase_8:
  action: "Generate PR + ticket comments"
  owner: "Orchestrator"
  gate: "READY_TO_MERGE"
```

---

## 🚨 PHASE DEFINITIONS

### PHASE 1: Context + Impact Analysis

**INPUT:**
- Ticket / requirement / bug description
- Graphify context (graph.json, analysis)

**ACTIONS:**
1. Query Graphify for related files, dependencies, modules
2. Identify impacted services / god nodes
3. Assess risk level (low / medium / high)
4. Determine change type (feature / bug / refactor)

**OUTPUT:**
```yaml
phase: impact_analysis
ticket_id: "PROJ-123"
description: "Brief summary"
impacted_files:
  - path: "backend/finance/app/api/account.py"
    reason: "Account CRUD endpoint"
    risk: "medium"
  - path: "backend/finance/app/services/account.py"
    reason: "Business logic for accounts"
    risk: "medium"

impacted_services:
  - Finance Module (Account service)
  - Sales Module (Account Dashboard sync)

impacted_god_nodes:
  - Account (61 edges - shared)
  - Logger (227 edges - logging impact)

dependencies:
  - SQLAlchemy ORM (existing)
  - Pydantic validation (existing)
  - PostgreSQL (existing)

risk_level: medium  # low | medium | high
change_type: feature  # feature | bug | refactor
recommended_mode: feature

reasoning: >
  Account is a god node shared by Finance & Sales.
  Any change must preserve backward compatibility.
  New API route requires integration tests.

graphify_sources:
  - graph.json (community: Finance Services)
  - GRAPH_REPORT.md (god nodes analysis)
```

**GATE:** ⏸️ WAIT_FOR_APPROVAL

---

### PHASE 2: Task Breakdown

**INPUT:**
- Impact analysis (PHASE 1)
- Project conventions (from [PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md))

**ACTIONS:**
1. Break requirement into atomic tasks
2. Assign type: code | test | doc | refactor
3. Identify dependencies between tasks
4. Estimate scope (T-shirt size: xs / s / m / l / xl)

**OUTPUT:**
```yaml
phase: task_breakdown
ticket_id: "PROJ-123"
mode: feature

tasks:
  - id: T1
    type: code
    description: "Update AccountCreate schema to include new_field"
    files:
      - backend/finance/app/schemas/account.py
    dependencies: []
    scope: xs  # < 15 min
    
  - id: T2
    type: code
    description: "Add new_field to Account ORM model"
    files:
      - backend/finance/app/models/account.py
    dependencies: [T1]
    scope: xs
    
  - id: T3
    type: code
    description: "Update AccountService.create() to handle new_field"
    files:
      - backend/finance/app/services/account.py
    dependencies: [T1, T2]
    scope: s
    
  - id: T4
    type: test
    description: "Write unit tests for AccountService.create() with new_field"
    files:
      - tests/finance/test_account_service.py
    dependencies: [T3]
    scope: s
    
  - id: T5
    type: doc
    description: "Update API docs + README with new_field usage"
    files:
      - backend/finance/app/api/account.py  # docstring
      - readme.md
    dependencies: [T3, T4]
    scope: xs

total_scope: "s (small - 1-2 hours)"
estimated_tokens: 800  # total for phases 3-4
```

**GATE:** ⏸️ WAIT_FOR_APPROVAL

---

### PHASE 3: Code Generation / Update

**INPUT:**
- Task breakdown (PHASE 2)
- Codebase conventions (Graphify + PATTERNS.md)

**ACTIONS:**
1. Generate code ONLY for approved task
2. Follow existing repo patterns (DI, layered architecture, naming)
3. Include error handling + validation
4. Add type hints + docstrings

**OUTPUT:**
```diff
# file: backend/finance/app/schemas/account.py
# Task: T1

@@ -5,6 +5,7 @@ class AccountCreate(BaseModel):
     name: str
     organization_id: int
     revenue_tier: Optional[str] = None
+    new_field: Optional[str] = None  # New field description

# file: backend/finance/app/models/account.py
# Task: T2

@@ -12,6 +12,7 @@ class Account(Base):
     organization_id: int = Column(Integer, ForeignKey("organization.id"))
     revenue_tier: str = Column(String(50), nullable=True)
+    new_field: str = Column(String(255), nullable=True)
```

**GATE:** ⏸️ WAIT_FOR_APPROVAL

---

### PHASE 4: Unit Test Generation

**INPUT:**
- Generated code (PHASE 3)
- Test conventions (pytest, fixtures, mocks)

**ACTIONS:**
1. Generate unit tests with happy path + error scenarios
2. Include edge cases and boundary conditions
3. Mock external dependencies (DB, S3, LLM)
4. Ensure ≥95% code coverage

**OUTPUT:**
```python
# file: tests/finance/test_account_service.py

def test_create_account_with_new_field():
    """Happy path: create account with new_field"""
    req = AccountCreate(
        name="Test Org",
        organization_id=1,
        new_field="value"
    )
    service = AccountService(db_mock)
    result = service.create(req)
    assert result.new_field == "value"

def test_create_account_new_field_optional():
    """Edge case: new_field is optional"""
    req = AccountCreate(name="Test Org", organization_id=1)
    service = AccountService(db_mock)
    result = service.create(req)
    assert result.new_field is None

def test_create_account_new_field_too_long():
    """Error case: new_field exceeds max length"""
    req = AccountCreate(
        name="Test Org",
        organization_id=1,
        new_field="x" * 300  # > 255
    )
    with pytest.raises(ValidationError):
        service.create(req)
```

**GATE:** ⏸️ WAIT_FOR_APPROVAL

---

### PHASE 5: Code Review (AI Self-Review)

**INPUT:**
- Generated code (PHASE 3)
- Generated tests (PHASE 4)

**ACTIONS:**
1. Validate logic correctness
2. Check for security vulnerabilities
3. Identify performance risks (N+1 queries, etc.)
4. Verify test coverage ≥95%
5. Check naming conventions match codebase

**OUTPUT:**
```yaml
phase: code_review
ticket_id: "PROJ-123"

logic_correctness: ✅ PASS
  - Account model correctly inherits from Base
  - Service layer properly validates input
  - Pydantic schema matches ORM model

security: ✅ PASS
  - No SQL injection (parameterized queries)
  - No hardcoded secrets
  - Input validation present

performance: ⚠️ WARNING
  issue: "N+1 query risk in AccountService.list()"
  severity: medium
  suggestion: "Add relationship eager loading with joinedload()"

test_coverage: ✅ PASS (95%)
  - Happy path ✅
  - Edge cases ✅
  - Error scenarios ✅

naming_conventions: ✅ PASS
  - CamelCase for classes ✅
  - snake_case for functions ✅
  - Docstrings present ✅

overall_risk: low
ready_to_merge: true

issues_found: 1  # warning, not blocking
suggestions: []  # actionable next steps
```

**GATE:** ⏸️ WAIT_FOR_APPROVAL

---

### PHASE 6: Bug Triage (IF BUG MODE)

**INPUT:**
- Bug description from ticket
- Impacted files (PHASE 1)

**ACTIONS:**
1. Classify severity (low / medium / high)
2. Trace root cause
3. Identify fix strategy (minimal, isolated change)
4. Assess regression risk

**OUTPUT:**
```yaml
phase: bug_triage
ticket_id: "BUG-456"

bug_title: "AccountService.create() fails with null organization_id"

root_cause:
  file: "backend/finance/app/services/account.py"
  line: 42
  issue: "Missing null check before accessing organization_id"
  code: "org_id = req.organization_id  # No validation"

severity: medium
  rationale: "Affects account creation, data validation should catch this"
  impact_scope: "Account service, only on invalid input"

affected_modules:
  - Finance Module (Account service)
  - API validation (should catch earlier)

fix_strategy: minimal
  - Add validation in AccountCreate schema (Pydantic)
  - Add null check in AccountService.create()
  - Add test to prevent regression

regression_risk: low
  rationale: "Adding validation is backward compatible"
  
priority: medium  # Based on severity + impact
```

**GATE:** ⏸️ WAIT_FOR_APPROVAL

---

### PHASE 7: Documentation

**INPUT:**
- Generated code (PHASE 3)
- Test cases (PHASE 4)

**ACTIONS:**
1. Update inline comments (ONLY where needed)
2. Update module docstrings
3. Update README / API docs
4. Add usage examples if needed

**OUTPUT:**
```md
# Changes Summary

## What Changed
- Updated `AccountCreate` schema to include `new_field: Optional[str]`
- Added `new_field` column to Account ORM model
- Updated `AccountService.create()` to persist new_field
- Added 3 new test cases for new_field handling

## Why Changed
- [PROJ-123] New requirement from Finance team
- New field enables tracking of custom account metadata

## Usage Example
```python
# Request
POST /api/v1/accounts
{
  "name": "Acme Corp",
  "organization_id": 1,
  "new_field": "custom metadata"
}

# Response
{
  "id": 42,
  "name": "Acme Corp",
  "new_field": "custom metadata",
  "created_at": "2026-05-07T..."
}
```

## Backward Compatibility
✅ new_field is optional (nullable) → no breaking changes
✅ Existing code continues to work

## Files Updated
- `backend/finance/app/schemas/account.py` (+5 lines)
- `backend/finance/app/models/account.py` (+1 line)
- `backend/finance/app/services/account.py` (+2 lines)
- `tests/finance/test_account_service.py` (+30 lines)
- `readme.md` (+8 lines in API docs section)
```

**GATE:** ⏸️ WAIT_FOR_APPROVAL

---

### PHASE 8: PR + Ticket Comments

**INPUT:**
- All previous phases output
- Code + tests + docs

**ACTIONS:**
1. Generate PR description (changes, impact, testing)
2. Generate ticket update comment (status, summary, next steps)

**OUTPUT:**
```md
## PR Summary

### Title
[PROJ-123] Add custom_field to Account schema

### Description
Adds optional `custom_field` to Account entity for tracking additional metadata.

**Changes:**
- Updated AccountCreate schema (Pydantic)
- Added custom_field column to Account model (SQLAlchemy)
- Updated AccountService.create() to persist custom_field
- Added 3 new unit tests

**Impact:**
- ✅ Backward compatible (new field is optional)
- ✅ No breaking API changes
- ✅ No database migration needed (column is nullable)
- 📊 ~10 lines of code change

**Testing:**
- ✅ Unit tests pass (3 new cases)
- ✅ Integration tests pass
- ✅ Edge cases covered (null, max length, etc.)

**Review Checklist:**
- [ ] Code follows repo conventions (naming, structure)
- [ ] All tests pass with ≥95% coverage
- [ ] No hardcoded secrets or config
- [ ] Error handling present
- [ ] Docstrings updated

---

## Ticket Update

**Status:** READY_FOR_REVIEW → (pending approval)

**Summary:**
Implemented custom_field addition to Account schema as requested in PROJ-123.

**Details:**
- ✅ Code generated + tested
- ✅ Self-review passed (logic, security, performance)
- ✅ Tests: 3 new cases (happy path, edge cases, errors)
- ✅ Docs updated

**Next Steps:**
1. Code review (assign to tech lead)
2. QA testing
3. Merge to main

**Artifacts:**
- PR: [link]
- Test coverage: 95%
- Risk level: low
```

**GATE:** ⏸️ READY_TO_MERGE (user decision)

---

## 🛠️ USAGE PATTERNS

### Pattern 1: Quick Feature (< 1 hour)
```
User: "@orchestrator create POST endpoint for /projects/{id}/risks"
Orchestrator:
  → PHASE 1 (Impact) → APPROVE
  → PHASE 2 (Breakdown: T1, T2, T3, T4) → APPROVE
  → Dispatch T1-T4 to @api-dev
  → PHASE 3-4 (Code + Tests) → APPROVE
  → PHASE 5 (Self-review) → APPROVE
  → PHASE 7-8 (Docs + PR) → READY_TO_MERGE
```

### Pattern 2: Production Bug (Medium Priority)
```
User: "BUG: AccountService.create() fails with null org_id"
Orchestrator:
  → PHASE 1 (Context) → APPROVE
  → PHASE 6 (Triage) → root cause identified → APPROVE
  → PHASE 3 (Fix) → APPROVE
  → PHASE 4 (Regression tests) → APPROVE
  → PHASE 5 (Verify) → APPROVE
  → PHASE 7-8 (Docs + PR) → READY_TO_MERGE
```

### Pattern 3: Large Refactor (Risky)
```
User: "@orchestrator refactor Finance module for N+1 optimization"
Orchestrator:
  → PHASE 1 (Scope + Risk) → APPROVE
  → PHASE 2 (Atomic tasks) → APPROVE
  → Dispatch to @api-dev
  → PHASE 3 (Refactor) → APPROVE
  → PHASE 4 (Regression tests - CRITICAL) → APPROVE
  → PHASE 5 (Verify behavior preserved) → APPROVE
  → PHASE 7-8 (Docs + PR) → READY_TO_MERGE
```

---

## 🔒 SAFETY GATES

**NEVER skip phases without explicit approval.**  
**ALWAYS halt at gate → wait for user decision.**  
**ALWAYS use Graphify context before PHASE 1.**

| Phase | Blocker? | Failure Mode | Recovery |
|-------|----------|-----------|----------|
| 1 | YES | Missing Graphify data | Re-query or ask for manual input |
| 2 | NO | Bad task breakdown | Replan in next iteration |
| 3 | YES | Generated code doesn't match convention | Regenerate with pattern reference |
| 4 | YES | Tests don't pass | Fix code or tests, re-run |
| 5 | NO | Review finds issue | Note in PR, proceed or fix |
| 6 | YES | Root cause unclear | Investigate more, delay fix |
| 7 | NO | Incomplete docs | Complete before merge |
| 8 | NO | PR template missing | Generate, then review |

---

## 📞 APPROVAL CHECKLIST

Before approving each phase, verify:

- ✅ **PHASE 1:** Graphify context fetched? Risk level acceptable?
- ✅ **PHASE 2:** Tasks are atomic? Dependencies clear? Scope realistic?
- ✅ **PHASE 3:** Code matches codebase patterns? No shortcuts taken?
- ✅ **PHASE 4:** Tests ≥95% coverage? Edge cases included?
- ✅ **PHASE 5:** No blocker issues found? Performance OK?
- ✅ **PHASE 6 (if bug):** Root cause identified? Fix strategy sound?
- ✅ **PHASE 7:** All docs updated? Usage examples clear?
- ✅ **PHASE 8:** PR template filled? Ticket closed?

---

## 🚨 EXCEPTIONS

### Trivial Tasks (T ≤ 15 min)
**May skip Phase 2 (Task Breakdown) if:**
- Scope is clearly xs (< 15 min)
- Single file, no cross-module impact
- Obvious fix / straightforward addition

**Still required:** PHASE 1 (Impact check)

### Hotfix Mode (Production Emergency)
**May compress phases 3-4-5 if:**
- P1 severity (production down)
- Fix is localized (1-2 files)
- Regression tests added BEFORE merge

**Still required:** PHASE 1 (validate fix scope), PHASE 6 (root cause)

---

## 📊 METRICS

Track for continuous improvement:

```yaml
metrics:
  avg_time_per_phase: "T1: 10min, T2: 15min, T3: 45min, T4: 30min, T5: 20min"
  approval_rate: "% of phases approved on first pass"
  rework_rate: "% of phases requiring revision"
  bug_escape_rate: "Bugs found post-merge / bugs caught in review"
  token_usage: "Avg tokens per feature / bug / refactor"
```

---

## 🔗 RELATED DOCS

- [../../PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md) — Project context, tech stack, conventions
- [../agents/AGENTS.md](../agents/AGENTS.md) — Agent specifications (source of truth)
- [../context/PATTERNS.md](../context/PATTERNS.md) — Codebase patterns (layered architecture, DI, error handling)
- [requirement-analysis.md](requirement-analysis.md) — Requirement parsing guide
