# Full Workflow — Complete 8-Phase SDLC

**Date:** 2026-05-07 | **Duration:** 2-3 hours for small features, 4-5 hours for large features

---

## 📋 Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ YOU SUBMIT A REQUIREMENT                                    │
│ (Ticket ID, description, priority, context)                │
└─────────────────┬───────────────────────────────────────────┘
                  ↓
        ┌─────────────────────┐
        │ PHASE 1             │
        │ Context + Impact    │
        │ Duration: 10-15 min │
        │ Owner: Orchestrator │
        └────────┬────────────┘
                 ↓ (Output: impact analysis YAML)
            ✅ YOU APPROVE
                 ↓
        ┌─────────────────────────────────┐
        │ PHASE 2 *                       │
        │ Task Breakdown                  │
        │ Duration: 15-20 min             │
        │ Owner: Orchestrator             │
        │ * Only if FEATURE or REFACTOR   │
        └────────┬────────────────────────┘
                 ↓ (Output: task breakdown T1, T2, T3...)
            ✅ YOU APPROVE
                 ↓
        ┌─────────────────────────────────┐
        │ PHASE 3                         │
        │ Code Generation                 │
        │ Duration: 45-60 min             │
        │ Owner: @api-dev OR @ai-arch     │
        └────────┬────────────────────────┘
                 ↓ (Output: code files, diffs)
            ✅ YOU APPROVE
                 ↓
        ┌─────────────────────────────────┐
        │ PHASE 4                         │
        │ Unit Test Generation            │
        │ Duration: 30-45 min             │
        │ Owner: @api-dev OR @ai-arch     │
        └────────┬────────────────────────┘
                 ↓ (Output: pytest code, ≥95% coverage)
            ✅ YOU APPROVE
                 ↓
        ┌─────────────────────────────────┐
        │ PHASE 5                         │
        │ Code Review (Self-Review)       │
        │ Duration: 20-30 min             │
        │ Owner: Orchestrator             │
        └────────┬────────────────────────┘
                 ↓ (Output: review findings YAML)
            ✅ YOU APPROVE
                 ↓
        ┌─────────────────────────────────┐
        │ PHASE 6 *                       │
        │ Bug Triage                      │
        │ Duration: 20-30 min             │
        │ Owner: Orchestrator             │
        │ * Only if BUG mode              │
        └────────┬────────────────────────┘
                 ↓ (Output: root cause analysis YAML)
            ✅ YOU APPROVE (if BUG mode)
                 ↓
        ┌─────────────────────────────────┐
        │ PHASE 7                         │
        │ Documentation                   │
        │ Duration: 20-30 min             │
        │ Owner: @api-dev OR @ai-arch     │
        └────────┬────────────────────────┘
                 ↓ (Output: updated docs, comments, README)
            ✅ YOU APPROVE
                 ↓
        ┌─────────────────────────────────┐
        │ PHASE 8                         │
        │ PR Generation & Merge           │
        │ Duration: 15-25 min             │
        │ Owner: Orchestrator             │
        └────────┬────────────────────────┘
                 ↓ (Output: PR ready to merge)
            ✅ YOU APPROVE & MERGE
                 ↓
        ┌─────────────────────────────────┐
        │ PR MERGED TO MAIN               │
        │ Ready to deploy when needed     │
        └─────────────────────────────────┘
```

---

## 🎯 Three Workflow Modes

### MODE 1: FEATURE (Typical)
**For:** New API endpoint, new insight type, new processor, new field  
**Phases:** 1 → 2 → 3 → 4 → 5 → 7 → 8  
**Duration:** 2-3 hours (small), 4-5 hours (large)  
**Example:** "Add custom_field to Account schema for Q2 reporting"

---

### MODE 2: BUG (Fix broken behavior)
**For:** Fix incorrect logic, handle edge case, security fix, performance issue  
**Phases:** 1 → 6 (triage) → 3 → 4 → 5 → 7 → 8  
**Duration:** 2-3 hours  
**Example:** "Account validation fails when custom_field is null"

---

### MODE 3: REFACTOR (Improve code, no behavior change)
**For:** Rename, reorganize, optimize, improve maintainability  
**Phases:** 1 → 2 → 3 → 4 (regression tests) → 5 → 7 → 8  
**Duration:** 2-4 hours  
**Example:** "Reorganize Account service into smaller modules"

---

## 📖 PHASE DETAILS

### PHASE 1: Context + Impact Analysis
**Duration:** 10-15 min  
**Owner:** Orchestrator  
**Input:** Your requirement (ticket_id, description, priority)  
**Process:** Orchestrator uses Graphify to analyze impact
- Identify related files & modules
- Find impacted god nodes (Account, Project, Logger, etc.)
- Assess risk (low/medium/high)
- Determine workflow mode (feature/bug/refactor)

**Output:** Impact analysis YAML
```yaml
phase: impact_analysis
impacted_files: 3-5 files
impacted_services: 1-2 services
risk_level: low|medium|high
change_type: feature|bug|refactor
```

**Gate:** ✅ YOU REVIEW & APPROVE

---

### PHASE 2: Task Breakdown & Planning
**Duration:** 15-20 min  
**Owner:** Orchestrator  
**When:** FEATURE or REFACTOR mode only (skipped for BUG)  
**Input:** Impact analysis  
**Process:** Break requirement into atomic tasks
- T1: Schema changes
- T2: Service layer updates
- T3: API endpoint changes
- T4: Tests
- T5: Documentation

**Output:** Task breakdown YAML
```yaml
tasks:
  - T1: "Modify Pydantic schema for Account"
    scope: "xs"
  - T2: "Update SQLAlchemy model"
    scope: "s"
  - T3: "Update service methods"
    scope: "m"
```

**Gate:** ✅ YOU REVIEW & APPROVE

---

### PHASE 3: Code Generation
**Duration:** 45-60 min  
**Owner:** @api-dev (API) OR @ai-arch (AI)  
**Input:** Task breakdown + code patterns  
**Process:** Generate code files
- Create/modify schemas, models, services, endpoints
- Create/modify crews, prompts, tools
- Follow codebase conventions

**Output:** Generated code (diffs ready to apply)

**Gate:** ✅ YOU REVIEW & APPROVE

---

### PHASE 4: Unit Test Generation
**Duration:** 30-45 min  
**Owner:** Same agent as PHASE 3  
**Input:** Generated code  
**Process:** Generate unit tests
- Happy path tests
- Edge case tests
- Error scenario tests
- Mocks for external calls
- Target: ≥95% code coverage

**Output:** pytest code with fixtures

**Gate:** ✅ YOU REVIEW & APPROVE

---

### PHASE 5: Code Review (Self-Review)
**Duration:** 20-30 min  
**Owner:** Orchestrator  
**Input:** Code + tests  
**Process:** AI-powered code review checklist
- Logic correctness ✅
- Security (no SQL injection, no secrets) ✅
- Performance (N+1 queries, caching) ✅
- Test coverage (≥95%) ✅
- Naming conventions ✅
- Pattern compliance ✅

**Output:** Code review findings YAML
```yaml
review_results:
  logic: "✅ pass"
  security: "✅ pass"
  performance: "⚠️ warn: N+1 in query loop"
  coverage: "✅ 96%"
```

**Gate:** ✅ YOU REVIEW & APPROVE

---

### PHASE 6: Bug Triage (BUG MODE ONLY)
**Duration:** 20-30 min  
**Owner:** Orchestrator  
**When:** BUG mode only  
**Input:** Bug description, reproduction steps, file references  
**Process:** Root cause analysis
- Trace execution path
- Identify root cause
- Assess severity (critical/high/medium/low)
- Propose minimal fix strategy
- Identify regression tests needed

**Output:** Bug triage YAML
```yaml
bug_id: "BUG-456"
root_cause: "Account validation fails when custom_field is null"
fix_strategy: "Add null check before validation"
severity: "high"
regression_tests: ["test_account_with_null_field"]
```

**Gate:** ✅ YOU REVIEW & APPROVE (then proceed to PHASE 3)

---

### PHASE 7: Documentation
**Duration:** 20-30 min  
**Owner:** Same agent as code generation  
**Input:** Generated code  
**Process:** Update documentation
- Update API docstrings (OpenAPI auto-gen)
- Update inline code comments
- Update README.md (if needed)
- Add usage examples
- Update Confluence/Wiki (if needed)

**Output:** Updated docs, comments, examples

**Gate:** ✅ YOU REVIEW & APPROVE

---

### PHASE 8: PR Generation & Merge
**Duration:** 15-25 min  
**Owner:** Orchestrator  
**Input:** All code, tests, docs  
**Process:** Generate PR
- Create GitHub PR from all changes
- Add PR description & acceptance criteria
- Link to Jira ticket
- Enable auto-merge

**Output:** PR ready to merge (or already merged)

**Gate:** ✅ YOU APPROVE & MERGE (or let CI/CD merge)

---

## ❓ FAQ

**Q: How long does this take?**  
A: 2-3 hours for small features (1-2 files changed), 4-5 hours for large features (5+ files, complex logic)

**Q: Can I skip phases?**  
A: No. All phases have approval gates to ensure quality.

**Q: Who are @api-dev and @ai-arch?**  
A: Copilot agents specialized in FastAPI development and AI/CrewAI development. See [agents/AGENTS.md](copilot/agents/AGENTS.md)

**Q: What if I disagree with the agent's output?**  
A: Reject at the gate, provide feedback, and it re-runs that phase.

**Q: Can multiple people work on the same requirement?**  
A: Yes. Phase 3 may spawn multiple agents (@api-dev for endpoints, @ai-arch for crews, etc.). They coordinate via handoff rules.

---

## 🔗 Related Docs

- **Quick reference:** [QUICK_START.md](QUICK_START.md)
- **Project context:** [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)
- **Entry point for requirements:** [copilot/instructions/requirement-analysis.md](copilot/instructions/requirement-analysis.md)
- **Phase-specific details:** [copilot/instructions/phases/](copilot/instructions/phases/)
- **Agent specifications:** [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md)
- **Code patterns:** [copilot/context/PATTERNS.md](copilot/context/PATTERNS.md)
