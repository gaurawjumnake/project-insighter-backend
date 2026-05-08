# Instructions Directory

**Purpose:** SDLC workflow definitions, phase templates, and requirement intake  
**Token Focus:** Load strategically - different templates for different phases

---

## 📂 Structure

```
instructions/
├── README.md (this file)
├── workflow-orchestrator.md ← Entry point, 8 phases, 3 modes
├── requirement-analysis.md ← Pre-Phase 1 intake & classification
│
└── phases/ ← Phase-specific files (token-optimized, 100-200 lines each)
    ├── PHASE-1-CONTEXT-IMPACT.md ← Graphify analysis, risk assessment
    ├── PHASE-2-TASK-BREAKDOWN.md ← Atomic task planning
    ├── PHASE-3-CODE-GENERATION.md ← API or AI code generation
    ├── PHASE-4-TESTING.md ← Unit test generation
    ├── PHASE-5-CODE-REVIEW.md ← AI self-review checklist
    ├── PHASE-6-BUG-TRIAGE.md ← Root cause analysis (BUG mode)
    ├── PHASE-7-DOCUMENTATION.md ← Docs, comments, README
    └── PHASE-8-PR-MERGE.md ← PR generation & merge checklist
```

---

## 📋 Quick Navigation

| File | Purpose | Load When | Size |
|------|---------|-----------|------|
| File | Purpose | Load When | Size |
|------|---------|-----------|------|
| **workflow-orchestrator.md** | Entry point, phase overview, SDLC modes | STARTING NEW TICKET | 200 lines |
| **requirement-analysis.md** | Requirement intake template, classification | RECEIVING NEW REQUEST | 150 lines |
| **phases/PHASE-1-CONTEXT-IMPACT.md** | Graphify analysis, impact assessment | PHASE 1 start | 120 lines |
| **phases/PHASE-2-TASK-BREAKDOWN.md** | Atomic task planning & decomposition | PHASE 2 start | 100 lines |
| **phases/PHASE-3-CODE-GENERATION.md** | Code generation (API or AI) | PHASE 3 start | 180 lines |
| **phases/PHASE-4-TESTING.md** | Unit test generation & coverage | PHASE 4 start | 160 lines |
| **phases/PHASE-5-CODE-REVIEW.md** | Code quality checklist & self-review | PHASE 5 start | 140 lines |
| **phases/PHASE-6-BUG-TRIAGE.md** | Bug root cause analysis (BUG mode) | PHASE 6 start | 150 lines |
| **phases/PHASE-7-DOCUMENTATION.md** | Documentation, comments, README | PHASE 7 start | 160 lines |
| **phases/PHASE-8-PR-MERGE.md** | PR generation & merge checklist | PHASE 8 start | 180 lines |

---

## 🔄 Workflow Entry Flow

```
1. REQUIREMENT COMES IN
   → Load: requirement-analysis.md
   → Use: Intake template, classify (feature/bug/refactor)
   
2. READY FOR PHASE 1
   → Load: workflow-orchestrator.md (PHASE 1 overview)
   → Then load: phases/PHASE-1-CONTEXT-IMPACT.md (template)
   
3. RUNNING EACH PHASE
   → Load: phases/PHASE-N-*.md (specific phase file)
   → Use: YAML/Python/Markdown template
   → Gate: WAIT_FOR_APPROVAL
   
4. COMPLETE & MERGE
   → Load: phases/PHASE-8-PR-MERGE.md
   → Generate: PR + ticket comments
   → Status: READY_TO_MERGE
```

---

## 📊 File Sizes & Token Load

| File | Lines | Load Priority | Typical Access |
|------|-------|---|---|
| workflow-orchestrator.md | 1,200 | HIGH | Every ticket |
| requirement-analysis.md | 600 | HIGH | Intake process |
| phases/PHASE-N-*.md | 100-200 each | HIGH | Each phase |

**Token Strategy:**
- Load `workflow-orchestrator.md` for every ticket
- Load `requirement-analysis.md` when intake needed
- Load `phases/PHASE-N-*.md` only for active phase (100-200 lines, not 1000+)

---

## 🎯 File Purpose Details

### [workflow-orchestrator.md](workflow-orchestrator.md)
**What it is:** Root workflow coordination guide  
**When to load:** Every ticket start, phase handoff, understanding SDLC  
**Key sections:**
- 8-phase SDLC overview (PHASE 1-8)
- Three workflow modes (FEATURE, BUG, REFACTOR)
- Gate policies (WAIT_FOR_APPROVAL, etc.)
- Agent responsibilities by phase
- Integration with project context & patterns

**Token size:** ~200 lines (lightweight)

---

### [workflow-orchestrator.md](workflow-orchestrator.md)
**What it is:** Complete SDLC workflow entry point  
**When to load:** Starting new work, need phase details, understanding gates  
**Key sections:**
- Quick start guide (3 steps for users/agents)
- Orchestrator responsibilities
- 8 SDLC phases (PHASE 1 through PHASE 8)
- 3 workflow modes (feature / bug / refactor)
- Safety gates & approval checkpoints
- Usage patterns & metrics

**Token size:** ~1,200 lines (large, but comprehensive)

---

### [requirement-analysis.md](requirement-analysis.md)
**What it is:** Pre-Phase 1 intake & classification system  
**When to load:** Receiving new ticket/requirement, need to classify work  
**Key sections:**
- Intake template (copy-paste)
- Classification rules (auto-detect: feature vs bug vs refactor)
- Scope estimation guide (xs/s/m/l/xl)
- Red flag escalation rules
- Requirement validation checklist
- 3 real-world examples

---

## 🚀 Individual Phase Files

Each phase has its own dedicated file (100-200 lines) for token efficiency:

| File | Purpose |
|------|---------|
| [phases/PHASE-1-CONTEXT-IMPACT.md](phases/PHASE-1-CONTEXT-IMPACT.md) | Impact analysis & risk assessment |
| [phases/PHASE-2-TASK-BREAKDOWN.md](phases/PHASE-2-TASK-BREAKDOWN.md) | Atomic task planning & decomposition |
| [phases/PHASE-3-CODE-GENERATION.md](phases/PHASE-3-CODE-GENERATION.md) | Code generation (API or AI) |
| [phases/PHASE-4-TESTING.md](phases/PHASE-4-TESTING.md) | Unit test generation & coverage |
| [phases/PHASE-5-CODE-REVIEW.md](phases/PHASE-5-CODE-REVIEW.md) | Code quality & security review |
| [phases/PHASE-6-BUG-TRIAGE.md](phases/PHASE-6-BUG-TRIAGE.md) | Bug root cause analysis (BUG mode only) |
| [phases/PHASE-7-DOCUMENTATION.md](phases/PHASE-7-DOCUMENTATION.md) | Documentation & comments |
| [phases/PHASE-8-PR-MERGE.md](phases/PHASE-8-PR-MERGE.md) | PR generation & merge |

**Load strategically:** Only load the phase file you're currently executing. Don't load all at once.

---

## 🚀 Usage Examples

### Scenario 1: New Feature Request
```
Incoming: "Add custom_field to Account for Q2 reporting"

1. Load: requirement-analysis.md
   → Use: Intake template
   → Classify: FEATURE (new field, new capability)
   
2. Load: workflow-orchestrator.md
   → Check: FEATURE mode sequence (1→2→3→4→5→7→8)
   
3. PHASE 1 → Load: phases/PHASE-1-CONTEXT-IMPACT.md
   → Use: Template, generate impact analysis YAML
   → Gate: WAIT_FOR_APPROVAL
   
4. PHASE 2 → Load: phases/PHASE-2-TASK-BREAKDOWN.md
   → Use: Template, break into atomic tasks
   → Gate: WAIT_FOR_APPROVAL
   
... (repeat for each phase)
```

### Scenario 2: Production Bug
```
Incoming: "AccountService.create() crashes with null org_id"

1. Load: requirement-analysis.md
   → Classify: BUG
   
2. Load: workflow-orchestrator.md
   → Check: BUG mode sequence (1→6→3→4→5→7→8)
   
3. PHASE 1 → Load: phases/PHASE-1-CONTEXT-IMPACT.md
4. PHASE 6 → Load: phases/PHASE-6-BUG-TRIAGE.md
   → Root cause analysis, fix strategy
   → Gate: WAIT_FOR_APPROVAL before proceeding to PHASE 3
```

### Scenario 3: Code Refactor
```
Incoming: "Optimize Finance queries for N+1 problem"

1. Classify: REFACTOR (optimization, zero behavior change)
2. Load: workflow-orchestrator.md (check REFACTOR sequence)
3. For each phase:
   → Load: phases/PHASE-N-*.md
   → PHASE 4 MUST include regression tests
```
```

---

## 📏 Token Optimization Strategy

### Minimal Load Path (Quick Classification)
```
Total tokens: ~100
1. Load: requirement-analysis.md (first 50 lines - intake template)
2. Load: workflow-orchestrator.md (first 30 lines - modes summary)
Result: Classify ticket, route to agent
```

### Standard Load Path (Full Workflow)
```
Total tokens: ~800
1. Load: PROJECT_CONTEXT.md (full - understand project)
2. Load: workflow-orchestrator.md (full - understand phases)
3. Load: phases/PHASE-N-*.md (specific phase file only)
Result: Complete phase execution
```

### Deep Dive Load Path (New Agent)
```
Total tokens: ~1,200
1. Load: PROJECT_CONTEXT.md (full - understand project)
2. Load: workflow-orchestrator.md (full - understand phases)
3. Load: phases/PHASE-N-*.md (specific phase - or load all phases as needed)
4. Load: agents/AGENTS.md (full - understand agent scope)
Result: Agent complete context
```

---

## 🔗 Related Directories

- **[../agents/](../agents/)** — Agent specifications
- **[../context/](../context/)** — Project patterns, architecture, integration guide
- **[../prompts/](../prompts/)** — LLM prompt templates (API design, crew design, etc.)
- **[../skills/](../skills/)** — Reusable skill definitions

---

## ✅ Quick Checklist

**Before starting PHASE 1:**
- ✅ Load: requirement-analysis.md (classify request)
- ✅ Load: workflow-orchestrator.md (understand phases & mode)
- ✅ Load: phases/PHASE-1-CONTEXT-IMPACT.md (PHASE 1 template)

**Before starting each phase:**
- ✅ Load: phases/PHASE-N-*.md (specific phase template)
- ✅ Load: agents/ specs (know which agent owns this phase)
- ✅ Review: Previous phase output

**Before dispatch to agent:**
- ✅ Load: agents/AGENTS.md (agent context)
- ✅ Load: context/PATTERNS.md (code patterns agent must follow)
- ✅ Prepare: Structured input per phase template
