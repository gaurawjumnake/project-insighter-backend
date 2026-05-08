# ROUTING.md — Task → Agent → Phase Mapping

**Date:** 2026-05-07 | **Version:** 1.0  
**Purpose:** Single source of truth for task routing, agent assignments, and phase mapping

---

## 📋 TASK ROUTING MATRIX

### TASK 1: REQUIREMENT ANALYSIS & INTAKE

| Dimension | Value |
|-----------|-------|
| **Task Name** | Requirement Analysis |
| **Phase(s)** | Pre-Phase 1 (intake) |
| **Agent** | User / Orchestrator |
| **Entry Point** | [copilot/instructions/requirement-analysis.md](copilot/instructions/requirement-analysis.md) |
| **Input** | Ticket ID, description, context |
| **Output** | Intake YAML, classification (feature/bug/refactor) |
| **Duration** | 5-10 min |

---

### TASK 2: CONTEXT + IMPACT ANALYSIS

| Dimension | Value |
|-----------|-------|
| **Task Name** | Context + Impact Analysis |
| **Phase** | 1 |
| **Agent** | Orchestrator |
| **Entry Point** | [copilot/instructions/phases/PHASE-1-CONTEXT-IMPACT.md](copilot/instructions/phases/PHASE-1-CONTEXT-IMPACT.md) |
| **Input** | Intake YAML + **Graphify Context** (MANDATORY) |
| **Graphify Data** | `graphify-out/GRAPH_REPORT.md` (report) + `graphify-out/graph.json` (raw data) |
| **Output** | Impact analysis YAML (god nodes, communities, risk, graphify sources) |
| **Duration** | 10-15 min |
| **Critical** | Load graphify-out/ files BEFORE analyzing impact |

---

### TASK 3: TASK BREAKDOWN & PLANNING

| Dimension | Value |
|-----------|-------|
| **Task Name** | Task Breakdown & Planning |
| **Phase** | 2 |
| **Agent** | Orchestrator |
| **Entry Point** | [copilot/instructions/phases/PHASE-2-TASK-BREAKDOWN.md](copilot/instructions/phases/PHASE-2-TASK-BREAKDOWN.md) |
| **Condition** | FEATURE or REFACTOR mode only (skipped for BUG) |
| **Input** | Impact analysis YAML |
| **Output** | Task breakdown YAML (T1, T2, T3...) |
| **Duration** | 15-20 min |

---

### TASK 4: CODE GENERATION (API)

| Dimension | Value |
|-----------|-------|
| **Task Name** | API Code Generation |
| **Phase** | 3 |
| **Agent** | **@api-dev** |
| **Entry Point** | [copilot/instructions/phases/PHASE-3-CODE-GENERATION.md](copilot/instructions/phases/PHASE-3-CODE-GENERATION.md) |
| **Trigger** | Task involves FastAPI endpoints, schemas, services, models |
| **Input** | Task breakdown, PATTERNS.md, reference code |
| **Output** | Generated code (schemas, models, services, endpoints) |
| **Duration** | 45-60 min |

---

### TASK 5: CODE GENERATION (AI)

| Dimension | Value |
|-----------|-------|
| **Task Name** | AI/Crew Code Generation |
| **Phase** | 3 |
| **Agent** | **@ai-arch** |
| **Entry Point** | [copilot/instructions/phases/PHASE-3-CODE-GENERATION.md](copilot/instructions/phases/PHASE-3-CODE-GENERATION.md) |
| **Trigger** | Task involves CrewAI crews, LLM prompts, AI pipelines |
| **Input** | Task breakdown, PATTERNS.md, reference crews |
| **Output** | Generated crew code, prompts, tools |
| **Duration** | 45-60 min |

---

### TASK 6: UNIT TEST GENERATION

| Dimension | Value |
|-----------|-------|
| **Task Name** | Unit Test Generation |
| **Phase** | 4 |
| **Agent** | **@api-dev** OR **@ai-arch** (same as PHASE 3 agent) |
| **Entry Point** | [copilot/instructions/phases/PHASE-4-TESTING.md](copilot/instructions/phases/PHASE-4-TESTING.md) |
| **Input** | Generated code from PHASE 3 |
| **Output** | pytest tests (≥95% coverage) |
| **Duration** | 30-45 min |
| **Note** | REFACTOR mode MUST include regression tests |

---

### TASK 7: CODE REVIEW (SELF-REVIEW)

| Dimension | Value |
|-----------|-------|
| **Task Name** | Code Review |
| **Phase** | 5 |
| **Agent** | Orchestrator |
| **Entry Point** | [copilot/instructions/phases/PHASE-5-CODE-REVIEW.md](copilot/instructions/phases/PHASE-5-CODE-REVIEW.md) |
| **Input** | Generated code + tests |
| **Output** | Review findings YAML (logic, security, performance, coverage) |
| **Duration** | 20-30 min |

---

### TASK 8: BUG TRIAGE (BUG MODE ONLY)

| Dimension | Value |
|-----------|-------|
| **Task Name** | Bug Triage |
| **Phase** | 6 |
| **Agent** | Orchestrator |
| **Entry Point** | [copilot/instructions/phases/PHASE-6-BUG-TRIAGE.md](copilot/instructions/phases/PHASE-6-BUG-TRIAGE.md) |
| **Condition** | BUG mode only (not feature/refactor) |
| **Input** | Bug description, reproduction steps, file references |
| **Output** | Root cause YAML, fix strategy, regression tests needed |
| **Duration** | 20-30 min |

---

### TASK 9: DOCUMENTATION

| Dimension | Value |
|-----------|-------|
| **Task Name** | Documentation |
| **Phase** | 7 |
| **Agent** | **@api-dev** OR **@ai-arch** (same as PHASE 3 agent) |
| **Entry Point** | [copilot/instructions/phases/PHASE-7-DOCUMENTATION.md](copilot/instructions/phases/PHASE-7-DOCUMENTATION.md) |
| **Input** | Generated code + tests |
| **Output** | Updated docs, comments, README, examples |
| **Duration** | 20-30 min |

---

### TASK 10: PR GENERATION & MERGE

| Dimension | Value |
|-----------|-------|
| **Task Name** | PR Generation & Merge |
| **Phase** | 8 |
| **Agent** | Orchestrator |
| **Entry Point** | [copilot/instructions/phases/PHASE-8-PR-MERGE.md](copilot/instructions/phases/PHASE-8-PR-MERGE.md) |
| **Input** | All code, tests, docs from phases 1-7 |
| **Output** | PR ready to merge (or merged) |
| **Duration** | 15-25 min |

---

## 🎯 PHASE → AGENT ROUTING

### PHASE 1: Context + Impact Analysis
- **Owner:** Orchestrator  
- **Agent:** None (orchestrator-owned)  
- **Trigger:** New ticket/requirement  
- **Entry:** [PHASE-1-CONTEXT-IMPACT.md](copilot/instructions/phases/PHASE-1-CONTEXT-IMPACT.md)

---

### PHASE 2: Task Breakdown
- **Owner:** Orchestrator  
- **Agent:** None (orchestrator-owned)  
- **Trigger:** After PHASE 1 approval (FEATURE or REFACTOR mode only)  
- **Entry:** [PHASE-2-TASK-BREAKDOWN.md](copilot/instructions/phases/PHASE-2-TASK-BREAKDOWN.md)

---

### PHASE 3: Code Generation
- **Owner:** Depends on task type
  - **@api-dev** if: API endpoints, schemas, services, database changes
  - **@ai-arch** if: CrewAI crews, LLM prompts, AI pipelines
  - **Orchestrator** if: Documentation, configuration changes
- **Entry:** [PHASE-3-CODE-GENERATION.md](copilot/instructions/phases/PHASE-3-CODE-GENERATION.md)
- **Load for agent:**
  - [context/PATTERNS.md](copilot/context/PATTERNS.md) (code patterns)
  - [agents/AGENTS.md](copilot/agents/AGENTS.md) (full agent specs)
  - [context/integration-guide.md](copilot/context/integration-guide.md) (if cross-module)

---

### PHASE 4: Unit Test Generation
- **Owner:** Same agent as PHASE 3
  - **@api-dev** if PHASE 3 = @api-dev or Orchestrator
  - **@ai-arch** if PHASE 3 = @ai-arch
- **Entry:** [PHASE-4-TESTING.md](copilot/instructions/phases/PHASE-4-TESTING.md)
- **Requirements:**
  - ≥95% code coverage
  - Happy path + edge cases + error scenarios
  - Mocks for external calls
  - Regression tests (REFACTOR mode)

---

### PHASE 5: Code Review
- **Owner:** Orchestrator  
- **Agent:** None (AI self-review)  
- **Entry:** [PHASE-5-CODE-REVIEW.md](copilot/instructions/phases/PHASE-5-CODE-REVIEW.md)
- **Validates:**
  - Logic correctness
  - Security (no SQL injection, no secrets)
  - Performance (N+1 queries, caching)
  - Test coverage (≥95%)
  - Naming conventions
  - Pattern compliance

---

### PHASE 6: Bug Triage
- **Owner:** Orchestrator  
- **Agent:** None (orchestrator-owned)  
- **Trigger:** BUG mode only  
- **Entry:** [PHASE-6-BUG-TRIAGE.md](copilot/instructions/phases/PHASE-6-BUG-TRIAGE.md)
- **Determines:**
  - Root cause analysis
  - Severity (critical/high/medium/low)
  - Fix strategy (minimal changes)
  - Regression risk
  - Regression tests needed

---

### PHASE 7: Documentation
- **Owner:** Same agent as PHASE 3
  - **@api-dev** if API changes (endpoint docs, examples)
  - **@ai-arch** if AI changes (crew docs, examples)
  - **Orchestrator** if docs-only changes
- **Entry:** [PHASE-7-DOCUMENTATION.md](copilot/instructions/phases/PHASE-7-DOCUMENTATION.md)
- **Updates:**
  - Inline code comments
  - API docstrings (OpenAPI auto-gen)
  - README.md
  - Usage examples

---

### PHASE 8: PR & Merge
- **Owner:** Orchestrator  
- **Agent:** None (orchestrator-owned)  
- **Entry:** [PHASE-8-PR-MERGE.md](copilot/instructions/phases/PHASE-8-PR-MERGE.md)
- **Creates:**
  - GitHub PR with description
  - Acceptance criteria
  - Jira ticket comment
  - Auto-merge enabled (if approved)

---

## 🔄 WORKFLOW MODES

### FEATURE Mode
**Phases:** 1 → 2 → 3 → 4 → 5 → 7 → 8  
**Agents:** Orchestrator → Orchestrator → (@api-dev OR @ai-arch) → ... → Orchestrator  
**Duration:** 2-3 hours (small), 4-5 hours (large)  
**Use case:** New API endpoint, new AI crew, new processor

---

### BUG Mode
**Phases:** 1 → 6 → 3 → 4 → 5 → 7 → 8  
**Agents:** Orchestrator → Orchestrator → (@api-dev OR @ai-arch) → ... → Orchestrator  
**Duration:** 2-3 hours  
**Use case:** Fix incorrect behavior, handle edge case, security fix

---

### REFACTOR Mode
**Phases:** 1 → 2 → 3 → 4 (regression) → 5 → 7 → 8  
**Agents:** Orchestrator → Orchestrator → (@api-dev OR @ai-arch) → ... → Orchestrator  
**Duration:** 2-4 hours  
**Use case:** Code optimization, refactoring, reorganization (zero behavior change)  
**Critical:** PHASE 4 MUST include regression tests to prove behavior preserved

---

## 🚀 AGENT SPECIALIZATIONS

### @api-dev (FastAPI Developer Agent)
- **Owns:** PHASE 3 (code gen), PHASE 4 (tests), PHASE 7 (docs) for API changes
- **Specialization:** FastAPI endpoints, Pydantic schemas, SQLAlchemy models, service layers, pytest
- **Entry Point:** [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md) (@api-dev section)

### @ai-arch (AI Architect Agent)
- **Owns:** PHASE 3 (code gen), PHASE 4 (tests), PHASE 7 (docs) for AI changes
- **Specialization:** CrewAI crews, LLM prompts, AI pipelines, multi-agent orchestration
- **Entry Point:** [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md) (@ai-arch section)

### Orchestrator (Workflow Engine)
- **Owns:** PHASE 1, 2, 5, 6, 8
- **Specialization:** Workflow management, phase coordination, approval gates, risk assessment
- **Entry Point:** [copilot/instructions/workflow-orchestrator.md](copilot/instructions/workflow-orchestrator.md)

---

## � AVAILABLE SKILLS (Reusable Components)

These skills accelerate code generation in PHASE 3 and should be loaded by agents as needed:

| Skill | Purpose | Used By | Location |
|-------|---------|---------|----------|
| **Endpoint Scaffold** | Generate FastAPI endpoints with full stack (schema → model → service → endpoint) | @api-dev | [copilot/skills/endpoint-scaffold/SKILL.md](copilot/skills/endpoint-scaffold/SKILL.md) |
| **Schema Analyzer** | Analyze & generate Pydantic schemas, SQLAlchemy models from requirements | @api-dev | [copilot/skills/schema-analyzer/SKILL.md](copilot/skills/schema-analyzer/SKILL.md) |
| **Crew Generator** | Generate CrewAI crew definitions, tasks, tools from crew design specs | @ai-arch | [copilot/skills/crew-generator/SKILL.md](copilot/skills/crew-generator/SKILL.md) |
| **Insight Pipeline Builder** | Generate end-to-end insight pipelines (intake → processing → output) | @ai-arch | [copilot/skills/insight-pipeline-builder/SKILL.md](copilot/skills/insight-pipeline-builder/SKILL.md) |

---

## �🔗 Quick Navigation

| I need to... | Go to... |
|---|---|
| Submit a requirement | [requirement-analysis.md](copilot/instructions/requirement-analysis.md) |
| Understand PHASE 1 | [PHASE-1-CONTEXT-IMPACT.md](copilot/instructions/phases/PHASE-1-CONTEXT-IMPACT.md) |
| Generate API code | [PHASE-3-CODE-GENERATION.md](copilot/instructions/phases/PHASE-3-CODE-GENERATION.md) + @api-dev from [AGENTS.md](copilot/agents/AGENTS.md) |
| Generate AI code | [PHASE-3-CODE-GENERATION.md](copilot/instructions/phases/PHASE-3-CODE-GENERATION.md) + @ai-arch from [AGENTS.md](copilot/agents/AGENTS.md) |
| Write unit tests | [PHASE-4-TESTING.md](copilot/instructions/phases/PHASE-4-TESTING.md) |
| Understand agent specs | [agents/AGENTS.md](copilot/agents/AGENTS.md) |
| Learn code patterns | [context/PATTERNS.md](copilot/context/PATTERNS.md) |
| Understand architecture | [context/codebase-snapshot.md](copilot/context/codebase-snapshot.md) + [context/integration-guide.md](copilot/context/integration-guide.md) |

---

**Last Updated:** 2026-05-07 | **Source of Truth:** Single file (ROUTING.md)
