# PHASE 1: Context + Impact Analysis

**Tokens:** ~200 | **Duration:** 10-15 min | **Owner:** Orchestrator + Graphify  
**Gate:** ⏸️ WAIT_FOR_APPROVAL

---

## 📋 INPUT

- Ticket / requirement / bug description (from requirement-analysis.md)
- **Graphify context (MANDATORY):**
  - `graphify-out/GRAPH_REPORT.md` — Human-readable god nodes, communities, metrics
  - `graphify-out/graph.json` — Raw node/edge relationships (917 nodes, 42 communities)
  - `graphify-out/cache/` — Individual module analysis files

---

## 🎯 ACTIONS

1. **Load Graphify REPORT:** Read `graphify-out/GRAPH_REPORT.md` for god nodes & communities overview
2. **Query Graphify DATA:** Use `graphify-out/graph.json` to find related files, dependencies, modules
3. **Identify impacted services** and god nodes (Account, Project, Logger, RevenueMaster, LlamaCloudDocumentParser)
4. **Assess risk level** (low / medium / high) — escalate if any god node involved
5. **Determine change type** (feature / bug / refactor)
6. **Map dependencies** (what this depends on, what depends on this)

---

## 📤 OUTPUT (YAML Format)

```yaml
phase: 1_context_impact_analysis
ticket_id: "PROJ-123"
title: "Add custom_field to Account schema"
description: "Brief 1-2 sentence summary of change"

impacted_files:
  - path: "backend/finance/app/api/account.py"
    reason: "Account CRUD endpoint"
    risk: "medium"
  - path: "backend/finance/app/services/account.py"
    reason: "Business logic for accounts"
    risk: "medium"
  - path: "backend/finance/app/models/account.py"
    reason: "ORM model definition"
    risk: "low"

impacted_services:
  - Finance Module (Account service)
  - Sales Module (Account Dashboard sync)
  - Insights Workflow (Account data integration)

impacted_god_nodes:
  - Account (61 edges) - CRITICAL: shared by Finance & Sales
  - Logger (227 edges) - logging impact only

dependencies:
  - SQLAlchemy ORM (existing - no version change needed)
  - Pydantic validation (existing - no version change needed)
  - PostgreSQL (existing - no schema migration required)

risk_assessment:
  level: medium  # low | medium | high
  rationale: "Account is god node. Must preserve backward compatibility."
  mitigation: "New field is optional (nullable). Existing clients unaffected."

change_type: feature  # feature | bug | refactor
recommended_mode: feature  # See workflow-orchestrator.md for modes

workflow_sequence:
  phases: [1, 2, 3, 4, 5, 7, 8]
  rationale: "Standard feature workflow"

graphify_sources:
  - graphify-out/graph.json (community: Finance Services, 917 nodes total)
  - graphify-out/GRAPH_REPORT.md (5 god nodes: Account, Project, Logger, RevenueMaster, LlamaCloudDocumentParser)
  - graphify-out/cache/*.json (individual module analysis)
  - copilot/context/codebase-snapshot.md (summarized god nodes & communities)
  - copilot/context/PATTERNS.md (code patterns via graphify)
```

---

## ✅ APPROVAL CHECKLIST

Before approving PHASE 1, verify:

- [ ] Graphify context loaded: `graphify-out/GRAPH_REPORT.md` reviewed
- [ ] Graph data checked: `graphify-out/graph.json` queried for impacted files
- [ ] Risk level acceptable for project
- [ ] Impacted services identified correctly (use graph communities)
- [ ] God nodes dependencies understood (5 god nodes: Account, Project, Logger, RevenueMaster, LlamaCloudDocumentParser)
- [ ] Change type correctly classified
- [ ] Recommended workflow mode appropriate

---

## 🚨 COMMON ISSUES

| Issue | Resolution |
|-------|-----------|
| Graphify data missing | Re-run: `uv run graphify analyze` (generates graphify-out/) |
| Risk too high (HIGH) | Escalate - involves god node or 5+ modules |
| Can't find impacted files | Query `graphify-out/graph.json` by module name or use `GRAPH_REPORT.md` |
| Change type unclear | Review requirement-analysis.md classification rules |
| Cross-module impact not obvious | Check `GRAPH_REPORT.md` "Communities" section for relationships |
| Graphify cache outdated | Refresh: `uv run graphify analyze` (1-2 min, updates all outputs)

---

## 📞 ESCALATION

If any of these apply, **PAUSE and escalate:**
- Risk level = HIGH
- Change affects 5+ core modules
- God node (Account, Project, Logger) modification
- Breaking API change identified
- Database schema migration required

---

## 🔗 NEXT STEP

→ Upon approval, proceed to **PHASE 2: Task Breakdown** (`phases/PHASE-2-TASK-BREAKDOWN.md`)
