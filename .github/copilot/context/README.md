# Context Directory

**Purpose:** Project context, patterns, architecture, and codebase knowledge  
**Token Focus:** Load selectively - avoid loading full context unless needed

---

## 📂 Structure

```
context/
├── README.md (this file)
├── PATTERNS.md ← Codebase patterns & conventions
├── integration-guide.md ← Cross-module data flows
├── codebase-snapshot.md ← Graphify analysis, god nodes, communities
└── [optional deeper context files]
```

---

## 📋 Quick Navigation

| File | Purpose | Load When | Size |
|------|---------|-----------|------|
| **PATTERNS.md** | Codebase conventions, layer patterns, DI, error handling | Implementing code (with agents) | 400 lines |
| **integration-guide.md** | Cross-module flows, data models, FK dependencies | Cross-module work, understanding relationships | 300 lines |
| **codebase-snapshot.md** | Graphify analysis, god nodes, communities, architecture | Need architectural overview | 300 lines |

---

## 🗺️ Codebase Map

### Graphify Analysis (In codebase-snapshot.md)
```
917 nodes · 2,464 edges · 42 communities

God Nodes (most connected):
1. Logger (227 edges) - omnipresent
2. Account (61 edges) - Finance ↔ Sales
3. Project (61 edges) - Finance ↔ Sales
4. RevenueMaster (50 edges) - Finance hub
5. LlamaCloudDocumentParser (31 edges) - AI hub
```

### Core Modules
```
backend/
├── finance/ - Revenue, KPI metrics, materialized views
├── sales/ - Dashboards, calendars, stakeholder management
├── doc_insighter/ - ⭐ SHARED AI ENGINE (LlamaParse + CrewAI)
├── insights_workflow/ - Async insights, multi-agent analysis
└── utilities/ - S3 storage, LLM models, logging
```

### Major Communities
- Utilities & Core (124 nodes) - Logging, async helpers
- Finance Services (106 nodes) - Account, Project, Revenue
- Sales Services (72 nodes) - Dashboards, allocations
- Document Processing (38 nodes) - LlamaParse, extraction
- Data Access Layer (38 nodes) - Queries, repositories
- Web Framework (49 nodes) - Pydantic schemas
- API Endpoints (39 nodes) - FastAPI routes
- AI Engine (18 nodes) - CrewAI, document analysis
- Storage & Cloud (31 nodes) - AWS, Azure integration

---

## 📋 File Details

### [PATTERNS.md](PATTERNS.md)
**What it is:** Codebase conventions and architectural patterns  
**Load when:** Implementing code, need reference patterns, reviewing for conventions  
**Key sections:**
- Layered Architecture (API → Service → Repo → ORM)
- Dependency Injection (FastAPI Depends)
- Error Handling (custom exceptions, HTTPException)
- Testing patterns (pytest fixtures, mocks)
- Performance patterns (eager loading, materialized views)
- Common pitfalls & fixes
- Reference files to study

**Example usage:**
```
Engineer: "Creating new Account endpoint"
→ Load: PATTERNS.md
→ Reference: Layered Architecture section
→ Study: backend/finance/app/api/account.py pattern
→ Generate: Following same pattern
```

**Token size:** ~400 lines (medium)

---

### [integration-guide.md](integration-guide.md)
**What it is:** Cross-module data flows and dependencies  
**Load when:** Working on multi-module features, understanding Account/Project sharing, designing new flows  
**Key sections:**
- Architecture diagram (Finance → Doc Insighter → Insights)
- Data flows (Document upload → Extraction → Storage)
- Account/Project CRUD with cross-module updates
- Insights generation (aggregated analysis)
- Shared data models (Account, Document)
- PostgreSQL FK dependencies
- Cross-module risks & implications

**Example usage:**
```
Engineer: "Account changes might affect Sales module?"
→ Load: integration-guide.md
→ Find: Shared Data Models section
→ Read: "Account is shared, both modules query same table"
→ Understand: NO data consistency issues (ACID guaranteed)
```

**Token size:** ~300 lines (small-medium)

---

### [codebase-snapshot.md](codebase-snapshot.md)
**What it is:** Graphify analysis output - structural overview  
**Load when:** Understanding architecture, god nodes, module cohesion, identifying impact scope  
**Key sections:**
- Corpus statistics (917 nodes, 2,464 edges, 42 communities)
- God nodes analysis (Logger, Account, Project, RevenueMaster, LlamaCloudDocumentParser)
- Community breakdown (Utilities, Finance, Sales, Document Processing, etc.)
- Surprising connections (unexpected dependencies)
- Hyperedges (group relationships)

**Example usage:**
```
Orchestrator: "PHASE 1: What services does Account change impact?"
→ Load: codebase-snapshot.md
→ Find: Account (61 edges, god node)
→ Read: "Shared across Finance, Sales"
→ Reference: Communities - Finance Services, Sales Services
→ Output: Impact analysis (Finance primary, Sales secondary)
```

**Token size:** ~300 lines (small-medium)

---

## 🚀 Usage Patterns

### Pattern 1: Code Generation (with @api-dev)
```
Task: "Create endpoint for account update"

1. Load: context/PATTERNS.md
   → Section: Layered Architecture
   → Reference: API layer pattern example
   
2. Load: context/codebase-snapshot.md
   → Understand: Account is god node (61 edges)
   → Caution: Shared by Finance & Sales
   
3. @api-dev generates code following PATTERNS.md
```

### Pattern 2: Cross-Module Feature (with Orchestrator)
```
Task: "New cross-module insight feature"

1. Load: context/integration-guide.md
   → Read: Account/Project CRUD with cross-module updates
   → Understand: Finance → Doc Insighter → Sales flow
   
2. Load: context/codebase-snapshot.md
   → Identify: Impacted communities (Finance + Sales + Insights)
   
3. Design: Multi-module flow, data dependencies
   → Output: PHASE 1 impact analysis referencing integration flows
```

### Pattern 3: Architecture Understanding (new team member)
```
Goal: "Understand codebase structure"

1. Load: context/codebase-snapshot.md (top-level overview)
   → Read: Core modules
   → Read: God nodes
   → Read: Major communities
   
2. Load: context/integration-guide.md (data flows)
   → Understand: How modules talk to each other
   
3. Load: context/PATTERNS.md (implementation patterns)
   → Study: How to add new features
```

---

## 📊 Token Optimization

| File | Lines | Load Priority | Typical Use |
|------|-------|---|---|
| PATTERNS.md | 400 | HIGH | Needed for every code generation |
| integration-guide.md | 300 | MEDIUM | Cross-module work only |
| codebase-snapshot.md | 300 | MEDIUM | Understanding architecture |

**Strategy:**
- Always load `PATTERNS.md` for code generation tasks
- Load `integration-guide.md` only for cross-module features
- Load `codebase-snapshot.md` for PHASE 1 impact analysis or new contributor onboarding

---

## 🔗 Related Directories

- **[../instructions/](../instructions/)** — SDLC workflow, phase templates
- **[../agents/](../agents/)** — Agent specs, phase mapping
- **[../prompts/](../prompts/)** — Prompt templates (crew design, API design, etc.)
- **[../skills/](../skills/)** — Reusable skills (crew generator, endpoint scaffold, etc.)

---

## 🧠 Mental Model

### When to Load What

**Minimal Context (Routing only):**
- Load: requirement-analysis.md (classify request)
- Result: Know which agent to route to

**Light Context (Code review/pattern check):**
- Load: PATTERNS.md
- Result: Agent can generate code following conventions

**Medium Context (Impact analysis):**
- Load: PATTERNS.md + codebase-snapshot.md
- Result: PHASE 1 impact analysis complete

**Heavy Context (Architecture work):**
- Load: PATTERNS.md + integration-guide.md + codebase-snapshot.md
- Result: Understand cross-module implications

---

## ✅ Pre-Flight Checklist

**Before PHASE 1 impact analysis:**
- ✅ Load: codebase-snapshot.md (understand god nodes & communities)
- ✅ Load: integration-guide.md (if multi-module)

**Before code generation (PHASE 3):**
- ✅ Load: PATTERNS.md (follow codebase conventions)
- ✅ Load: integration-guide.md (if cross-module impacts)

**Before new feature design:**
- ✅ Load: codebase-snapshot.md (identify impact scope)
- ✅ Load: integration-guide.md (data flow implications)
- ✅ Load: PATTERNS.md (implementation patterns)
