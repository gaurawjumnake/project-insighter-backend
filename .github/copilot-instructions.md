# Copilot Instructions — Gated SDLC Workflow

**Date:** 2026-05-07 | **Version:** 1.0  
**Status:** ✅ Active Entry Point for All Workflow Operations

---

## 🎯 PRIMARY ENTRY POINT

This file guides all Copilot-driven workflow operations. Use this to understand:
- Task routing (requirement → agent → phase)
- Agent responsibilities & specializations
- Phase execution sequence
- Approval gates & handoff rules

---

## 🚀 QUICK NAVIGATION BY SCENARIO

### Scenario 1: I Have a New Requirement
**Time:** 30 seconds to submit  
**Path:**
1. Read: [QUICK_START.md](QUICK_START.md) (30 sec overview)
2. Use: [copilot/instructions/requirement-analysis.md](copilot/instructions/requirement-analysis.md) (intake template)
3. Submit intake YAML with ticket details

→ **Orchestrator routes to PHASE 1**

---

### Scenario 2: I'm an Agent (Execute a Phase)
**Time:** Varies by phase (10-60 min)  
**Path:**
1. Find your task in: [ROUTING.md](ROUTING.md) (task → agent → phase mapping)
2. Load: [copilot/instructions/phases/PHASE-N-*.md](copilot/instructions/phases/) (specific phase file)
3. Load agent context: [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md) (your agent specs)
4. Load patterns: [copilot/context/PATTERNS.md](copilot/context/PATTERNS.md) (code patterns)
5. Execute phase per template

→ **Output ready for approval gate**

---

### Scenario 3: I'm the Orchestrator (Manage Workflow)
**Time:** Continuous coordination  
**Path:**
1. Load: [ROUTING.md](ROUTING.md) (task routing, workflow modes)
2. Load: [copilot/instructions/workflow-orchestrator.md](copilot/instructions/workflow-orchestrator.md) (orchestrator playbook)
3. For each phase:
   - Load: [copilot/instructions/phases/PHASE-N-*.md](copilot/instructions/phases/) (phase details)
   - Route to responsible agent
   - Collect output
   - Gate: Approval required before proceeding

→ **All phases executed, PR ready to merge**

---

## 📋 ROUTING REFERENCE

**Task → Phase → Agent Mapping:**

| Task | Phase | Agent | Duration |
|------|-------|-------|----------|
| Intake | Pre-1 | User | 5-10 min |
| Context + Impact | 1 | Orchestrator | 10-15 min |
| Task Breakdown | 2 | Orchestrator | 15-20 min |
| Code Generation | 3 | @api-dev OR @ai-arch | 45-60 min |
| Unit Tests | 4 | @api-dev OR @ai-arch | 30-45 min |
| Code Review | 5 | Orchestrator | 20-30 min |
| Bug Triage* | 6 | Orchestrator | 20-30 min |
| Documentation | 7 | @api-dev OR @ai-arch | 20-30 min |
| PR & Merge | 8 | Orchestrator | 15-25 min |

*Phase 6 only for BUG mode

**Full details:** [ROUTING.md](ROUTING.md)

---

## 🎯 WORKFLOW MODES

### FEATURE Mode
**Phases:** 1 → 2 → 3 → 4 → 5 → 7 → 8  
**Use:** New API endpoint, new AI crew, new field, new processor  
**Duration:** 2-3 hours (small), 4-5 hours (large)  
**Example:** "Add custom_field to Account schema for Q2 reporting"

### BUG Mode
**Phases:** 1 → 6 (triage) → 3 → 4 → 5 → 7 → 8  
**Use:** Fix incorrect behavior, edge case, security issue  
**Duration:** 2-3 hours  
**Example:** "Account validation fails when custom_field is null"

### REFACTOR Mode
**Phases:** 1 → 2 → 3 → 4 (regression) → 5 → 7 → 8  
**Use:** Code optimization, reorganization (zero behavior change)  
**Duration:** 2-4 hours  
**Example:** "Optimize Finance queries for N+1 problem"

**Full workflow diagram:** [FULL_WORKFLOW.md](FULL_WORKFLOW.md)

---

## 🤖 AGENT SPECIALIZATIONS

### @api-dev (FastAPI Developer)
- **Owns:** PHASE 3 (code gen), PHASE 4 (tests), PHASE 7 (docs) for API changes
- **Specialization:** FastAPI endpoints, Pydantic schemas, SQLAlchemy models, pytest
- **Entry Point:** [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md) (@api-dev section)

### @ai-arch (AI Architect)
- **Owns:** PHASE 3 (code gen), PHASE 4 (tests), PHASE 7 (docs) for AI changes
- **Specialization:** CrewAI crews, LLM prompts, AI pipelines, multi-agent orchestration
- **Entry Point:** [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md) (@ai-arch section)

### Orchestrator (Workflow Engine)
- **Owns:** PHASE 1, 2, 5, 6, 8
- **Specialization:** Workflow management, phase coordination, approval gates
- **Entry Point:** [copilot/instructions/workflow-orchestrator.md](copilot/instructions/workflow-orchestrator.md)

---

## 📂 ESSENTIAL FILES BY ROLE

### 🚀 New Agent / First-Time User
Load in order (90 min total onboarding):
1. [QUICK_START.md](QUICK_START.md) — 2 min
2. [FULL_WORKFLOW.md](FULL_WORKFLOW.md) — 20 min
3. [ROUTING.md](ROUTING.md) — 15 min
4. [copilot/context/codebase-snapshot.md](copilot/context/codebase-snapshot.md) — 30 min
5. [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md) — 15 min
6. [copilot/context/PATTERNS.md](copilot/context/PATTERNS.md) — 10 min

### 🔧 Executing a Phase
Load only what you need:
1. This file (copilot-instructions.md) — 5 min
2. [copilot/instructions/phases/PHASE-N-*.md](copilot/instructions/phases/) — 5-10 min
3. [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md) (your agent section) — 5 min
4. [copilot/context/PATTERNS.md](copilot/context/PATTERNS.md) — 10 min

### 🎛️ Orchestrator (Workflow Management)
Load strategically:
1. This file (copilot-instructions.md) — 5 min
2. [ROUTING.md](ROUTING.md) — 10 min
3. [copilot/instructions/workflow-orchestrator.md](copilot/instructions/workflow-orchestrator.md) — 20 min
4. Phase files as needed: [copilot/instructions/phases/](copilot/instructions/phases/) — 5-10 min per phase

### 📝 Submitting a Requirement
Load minimal:
1. [QUICK_START.md](QUICK_START.md) — 2 min
2. [copilot/instructions/requirement-analysis.md](copilot/instructions/requirement-analysis.md) — 5 min
3. Fill intake template

---

## 🔌 KEY INTEGRATION POINTS

### Requirement Submission Entry Point
→ [copilot/instructions/requirement-analysis.md](copilot/instructions/requirement-analysis.md)  
**Action:** Copy intake template, fill details, submit

### Phase Execution Entry Point
→ [copilot/instructions/phases/PHASE-N-*.md](copilot/instructions/phases/)  
**Action:** Load specific phase file for your phase number

### Code Generation Context
→ [copilot/context/PATTERNS.md](copilot/context/PATTERNS.md)  
**Action:** Reference patterns before coding

### Architecture Context
→ [copilot/context/codebase-snapshot.md](copilot/context/codebase-snapshot.md)  
**Action:** Understand god nodes, communities, tech stack

### Task Routing Decision
→ [ROUTING.md](ROUTING.md)  
**Action:** Find task → phase → agent mapping

### Graphify Context (MANDATORY for PHASE 1)
→ [graphify-out/GRAPH_REPORT.md](../graphify-out/GRAPH_REPORT.md) (human-readable report)  
→ [graphify-out/graph.json](../graphify-out/graph.json) (raw graph data)  
**Action:** Load context before PHASE 1 to identify impacted modules, god nodes, communities

---

## 🔍 GRAPHIFY USAGE IN WORKFLOW

**PHASE 1 (Context + Impact Analysis)** requires Graphify context:
- Impact Analysis: Which files/services are impacted
- God Nodes Detection: Account, Project, Logger, RevenueMaster, etc.
- Communities: Finance Services, Sales Services, Doc Processing, etc.
- Risk Assessment: Medium/High risk if god nodes involved

---

## ✅ APPROVAL GATES

**All phases require approval before proceeding:**

```
PHASE 1 Output → ✅ YOU APPROVE → PHASE 2
PHASE 2 Output → ✅ YOU APPROVE → PHASE 3
PHASE 3 Output → ✅ YOU APPROVE → PHASE 4
PHASE 4 Output → ✅ YOU APPROVE → PHASE 5
PHASE 5 Output → ✅ YOU APPROVE → PHASE 6/7*
PHASE 6 Output → ✅ YOU APPROVE → PHASE 3 (BUG only)
PHASE 7 Output → ✅ YOU APPROVE → PHASE 8
PHASE 8 Output → ✅ YOU APPROVE & MERGE
```

*Phase 6 only for BUG mode; skip to PHASE 7 for FEATURE/REFACTOR

---

## 📊 EXPECTED DURATIONS

| Scenario | Total Time | Phases |
|----------|-----------|--------|
| Small feature | 2-3 hours | 1→2→3→4→5→7→8 |
| Large feature | 4-5 hours | 1→2→3→4→5→7→8 |
| Production bug | 2-3 hours | 1→6→3→4→5→7→8 |
| Code refactor | 2-4 hours | 1→2→3→4→5→7→8 |
| Hotfix | 1-2 hours | 1→3→4→5→7→8 (skip phases 2, 6) |

---

## 🔗 QUICK LOOKUP TABLE

| I need to... | Load this |
|---|---|
| Submit a requirement | [requirement-analysis.md](copilot/instructions/requirement-analysis.md) |
| Understand the workflow | [FULL_WORKFLOW.md](FULL_WORKFLOW.md) + [ROUTING.md](ROUTING.md) |
| Route a task to an agent | [ROUTING.md](ROUTING.md) |
| Understand my agent's role | [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md) |
| Execute PHASE N | [copilot/instructions/phases/PHASE-N-*.md](copilot/instructions/phases/) |
| Learn code patterns | [copilot/context/PATTERNS.md](copilot/context/PATTERNS.md) |
| Understand architecture | [copilot/context/codebase-snapshot.md](copilot/context/codebase-snapshot.md) |
| Learn cross-module flows | [copilot/context/integration-guide.md](copilot/context/integration-guide.md) |
| Manage workflow as Orchestrator | [workflow-orchestrator.md](copilot/instructions/workflow-orchestrator.md) |
| Get quick 30-sec reference | [QUICK_START.md](QUICK_START.md) |

---

## 🎓 BOOTSTRAP SEQUENCE

### Day 1: Foundation (2 hours)
1. Read: [QUICK_START.md](QUICK_START.md) (2 min)
2. Read: [FULL_WORKFLOW.md](FULL_WORKFLOW.md) (20 min)
3. Read: [ROUTING.md](ROUTING.md) (15 min)
4. Study: [copilot/context/codebase-snapshot.md](copilot/context/codebase-snapshot.md) (30 min)
5. Read: [copilot/context/PATTERNS.md](copilot/context/PATTERNS.md) (15 min)

### Day 2: Agent Specialization (1 hour)
1. Load: [copilot/agents/AGENTS.md](copilot/agents/AGENTS.md) (your agent section)
2. Load: [copilot/instructions/phases/PHASE-3-CODE-GENERATION.md](copilot/instructions/phases/PHASE-3-CODE-GENERATION.md)
3. Load: [copilot/context/PATTERNS.md](copilot/context/PATTERNS.md) (deep dive)

### Day 3: First Ticket
1. Read: [copilot/instructions/requirement-analysis.md](copilot/instructions/requirement-analysis.md)
2. Execute: Your assigned phase using [copilot/instructions/phases/PHASE-N-*.md](copilot/instructions/phases/)

---

## 📚 REFERENCE

**For complete documentation structure, see:** [README.md](README.md) (informational only)

**For specific workflows, see:**
- [QUICK_START.md](QUICK_START.md) — 30-second reference
- [FULL_WORKFLOW.md](FULL_WORKFLOW.md) — Complete 8-phase guide with diagrams
- [ROUTING.md](ROUTING.md) — Task-to-agent-to-phase mapping

---

**Last Updated:** 2026-05-07 | **Status:** ✅ Active  
**Entry Point for:** All Copilot workflow operations
