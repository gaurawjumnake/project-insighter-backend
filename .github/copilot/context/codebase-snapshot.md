# Codebase Snapshot — Graphify Analysis

**Date:** 2026-05-07 | **Source:** Graphify analysis (graphify-out/GRAPH_REPORT.md)  
**Purpose:** Architectural overview, god nodes, communities, connection map  
**Token Focus:** Quick reference for impact analysis, architecture understanding

---

## 📊 Corpus Statistics

- **Total Nodes:** 917
- **Total Edges:** 2,464
- **Communities Detected:** 42
- **Total Words:** ~49,006
- **Extraction Quality:** 42% EXTRACTED · 58% INFERRED · 0% AMBIGUOUS
- **Average Confidence:** 0.6 (for inferred edges)
- **Token Cost:** 2,847 input

**Implication:** Corpus fits in single context window. Well-structured codebase with clear patterns.

---

## 🔴 God Nodes (Most Connected - Core Abstractions)

These are your core abstractions. Changes here affect many parts.

| Rank | Node | Edges | Purpose | Impact |
|------|------|-------|---------|--------|
| 1 | **Logger** | 227 | Logging infrastructure | Omnipresent - used everywhere |
| 2 | **Account** | 61 | Organization customer | Shared Finance ↔ Sales |
| 3 | **Project** | 61 | Client engagement | Shared Finance ↔ Sales |
| 4 | **RevenueMaster** | 50 | Finance analytics hub | Central to revenue tracking |
| 5 | **PrivateEquity** | 40 | PE fund management | Finance module |
| 6 | **ProjectDocument** | 37 | Document storage | Bridges document extraction |
| 7 | **LlamaCloudDocumentParser** | 31 | AI extraction hub | Central to document analysis |
| 8 | **ProjectSummary** | 31 | Project analysis | Analytics output |
| 9 | **DeliveryUnit** | 30 | Team allocation | Sales module |
| 10 | **DeliveryUnitOut** | 29 | Response schema | Sales API |

**Key Insights:**
- **Logger (227 edges)** — ANY change to logging affects multiple modules
- **Account (61 edges)** — Shared by Finance & Sales, CRITICAL impact zone
- **Project (61 edges)** — Shared by Finance & Sales, CRITICAL impact zone
- **LlamaCloudDocumentParser (31 edges)** — AI hub, many extraction workflows depend on it

---

## 🗂️ Major Communities (Grouped By Cohesion)

### Community 0: Utilities & Core (124 nodes, cohesion: 0.03)
**Purpose:** Logging, async helpers, app utilities  
**Key Components:** Logger, app_utilities, async_pool_executor  
**Impact:** Cross-cutting - used by all modules  

### Community 1: Finance Services (106 nodes, cohesion: 0.06)
**Purpose:** Account, project, revenue models & APIs  
**Key Components:** Account, Project, RevenueMaster, AccountMetricsMV, Revenue tracking, KPI metrics  
**Impact:** PRIMARY module for financial data  

### Community 2: Sales Services (72 nodes, cohesion: 0.04)
**Purpose:** Dashboards, calendars, stakeholder management  
**Key Components:** AccountDashboard, Calendar, Stakeholder, Team allocation  
**Impact:** Sales module, uses shared Account model  

### Community 3: Document Processing (38 nodes, cohesion: 0.05)
**Purpose:** Document extraction, LlamaParse integration, extraction pipeline  
**Key Components:** LlamaCloudDocumentParser, extraction pipeline, document processing  
**Impact:** Hub for document analysis (AI engine)  

### Community 4: Data Access Layer (38 nodes, cohesion: 0.07)
**Purpose:** Data queries, repositories, document retrieval  
**Key Components:** Query patterns, service methods, repository functions  
**Impact:** Data access abstraction  

### Community 5: Web Framework (49 nodes, cohesion: 0.08)
**Purpose:** Pydantic schemas, request/response validation  
**Key Components:** AccountBase, AccountCreate, AccountOut, response models  
**Impact:** API validation layer  

### Community 6: API Endpoints (39 nodes, cohesion: 0.06)
**Purpose:** FastAPI routes, insight agents, endpoint handlers  
**Key Components:** Router definitions, endpoint handlers, insight service APIs  
**Impact:** External API surface  

### Community 7: Schema Validation (17 nodes, cohesion: 0.06)
**Purpose:** Pydantic base classes, validation rules  
**Key Components:** BaseModel definitions, field validators  
**Impact:** Validation infrastructure  

### Community 8: AI Engine (18 nodes, cohesion: 0.08)
**Purpose:** CrewAI orchestration, document analysis, extraction  
**Key Components:** DataExtractor, PDFToMarkdown, agent creation, task definition  
**Impact:** AI-driven analysis hub  

### Community 9: Storage & Cloud (31 nodes, cohesion: 0.08)
**Purpose:** AWS S3, Azure integration, cloud infrastructure  
**Key Components:** AWS Lambda, S3 storage, Azure OpenAI, CloudFront  
**Impact:** Deployment & storage layer  

### Community 10-41: Specialized Communities (varying cohesion)
**Includes:** Private Equity CRUD, Calendar events, File operations, Config, etc.

---

## 🔗 Surprising Connections (Inferred Dependencies)

These are unexpected relationships discovered by Graphify:

1. **Account Dashboard → Base**
   - `backend\sales\app\models\account_dashboard.py` uses Base
   - Implies: Dashboard model inherits ORM layer

2. **LlamaParse → Logger**
   - `backend\doc_insighter\core\llama_parsing.py` uses Logger
   - Implies: Document extraction logs extraction operations

3. **File Reader Tool → Logger**
   - `backend\doc_insighter\tools\file_reader_tool.py` uses Logger
   - Implies: File operations are logged

**Implication:** Logging is more tightly integrated than initially obvious. Changes to Logger affect document processing.

---

## 📈 Hyperedges (Group Relationships)

These are cohesive groups of related concepts:

### Document Processing Pipeline
- readme_DocumentUploadWorkflow
- readme_DocumentProcessor
- readme_DocInsighterModule
- readme_S3Bucket

**Flow:** Upload → Process → Doc Insighter → Storage

### AI-Powered Analysis Stack
- readme_AzureOpenAI
- readme_CrewAI
- readme_LlamaParse
- readme_DocInsighterModule

**Stack:** LlamaParse + CrewAI + Azure OpenAI = Document analysis engine

### Shared Data & Services
- readme_FinanceModule
- readme_SalesModule
- readme_DocInsighterModule
- readme_PostgreSQL

**Architecture:** Finance & Sales both use Doc Insighter (SHARED) and PostgreSQL

---

## 🏗️ Architecture Map

```
┌─────────────────────────────────────────────────┐
│ API Layer (FastAPI + Pydantic)                  │
│ ├─ Finance API routes                           │
│ ├─ Sales API routes                             │
│ └─ Insights API routes                          │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│ Service & Business Logic Layer                  │
│ ├─ Finance Service (Account, Revenue, KPI)      │
│ ├─ Sales Service (Dashboard, Calendar)          │
│ ├─ Insights Service (Aggregation)               │
│ └─ Document Processing Service                  │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│ Data Access & Document Processing Layer         │
│ ├─ Repository Pattern (Queries)                 │
│ ├─ LlamaParse (Document Extraction)             │
│ ├─ CrewAI (Multi-agent Analysis)                │
│ └─ File Reader (Document Upload)                │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│ Data & Infrastructure Layer                     │
│ ├─ PostgreSQL (Shared Data)                     │
│ ├─ AWS S3 (Document Storage)                    │
│ ├─ Azure OpenAI (LLM)                           │
│ └─ AWS Lambda (Serverless Compute)              │
└─────────────────────────────────────────────────┘
```

---

## 🌐 Module Dependencies (At A Glance)

```
Finance Module
    ├─ Account (shared with Sales)
    ├─ Project (shared with Sales)
    ├─ Revenue
    ├─ RevenueMaster (god node)
    └─ Doc Insighter (SHARED AI ENGINE)

Sales Module
    ├─ Account (shared with Finance)
    ├─ Project (shared with Finance)
    ├─ AccountDashboard
    ├─ DeliveryUnit
    ├─ Calendar
    └─ Doc Insighter (SHARED AI ENGINE)

Doc Insighter (SHARED)
    ├─ LlamaParse (extraction)
    ├─ CrewAI (analysis)
    └─ S3 Storage

Insights Workflow
    ├─ Finance data aggregation
    ├─ Sales data aggregation
    ├─ Document analysis
    └─ S3 staging
```

---

## 🎯 Impact Analysis Quick Reference

### If changing Account model:
- ✅ Finance module (primary)
- ✅ Sales module (Account Dashboard)
- ⚠️ Insights workflow (if account-specific)
- **Risk:** HIGH (god node, 61 edges)

### If changing Project model:
- ✅ Finance module (revenue tracking)
- ✅ Sales module (team allocation)
- ✅ Doc Insighter (project documents)
- **Risk:** HIGH (god node, 61 edges)

### If changing Logger:
- ✅ ALL modules (227 edges)
- **Risk:** CRITICAL (omnipresent)

### If changing LlamaCloudDocumentParser:
- ✅ Doc Insighter module (primary)
- ✅ Finance document processing
- ✅ Sales document processing
- ✅ Insights workflow
- **Risk:** HIGH (extraction hub, 31 edges)

### If changing RevenueMaster:
- ✅ Finance module (primary)
- ✅ Insights workflow (aggregation)
- **Risk:** MEDIUM-HIGH (analytics hub, 50 edges)

---

## 📌 Community Cohesion Analysis

| Community | Cohesion | Assessment | Implication |
|-----------|----------|------------|-------------|
| Utilities & Core | 0.03 | Low | Loosely coupled, infrastructure-level |
| Finance Services | 0.06 | Low | Distributed, multiple responsibilities |
| Sales Services | 0.04 | Low | Distributed across module |
| Document Processing | 0.05 | Low | Modular, well-separated concerns |
| Data Access Layer | 0.07 | Low | Repository pattern, loosely coupled |
| Web Framework | 0.08 | Low-Medium | Schemas somewhat isolated |
| API Endpoints | 0.06 | Low | Routes are distributed |
| Schema Validation | 0.06 | Low | Validation is modular |
| AI Engine | 0.08 | Low-Medium | AI concerns are grouped |
| Storage & Cloud | 0.08 | Low-Medium | Infrastructure grouped |

**Overall Implication:** Low cohesion across communities = well-modularized code. High modularity = changes are localized, but shared entities (Account, Project) require careful cross-module coordination.

---

## 🚨 Risk Zones (Red Flags for Changes)

| Zone | Risk | Reason | Mitigation |
|------|------|--------|-----------|
| **Logger** | CRITICAL | 227 edges, omnipresent | Don't change. Use extension points only. |
| **Account** | HIGH | 61 edges, shared Finance ↔ Sales | Test Finance + Sales after changes. |
| **Project** | HIGH | 61 edges, shared Finance ↔ Sales | Test Finance + Sales after changes. |
| **LlamaCloudDocumentParser** | HIGH | 31 edges, AI hub | Regression test all extractors. |
| **RevenueMaster** | MEDIUM-HIGH | 50 edges, analytics hub | Test revenue flows in Finance. |
| **Integration points** | MEDIUM | Finance → Doc Insighter → Sales | Test data flow end-to-end. |

---

## 🎓 Learning Paths

### Understanding Finance Module
1. Study: Account + Project (god nodes)
2. Study: RevenueMaster (50 edges, analytics hub)
3. Study: Finance services (106 nodes)

### Understanding Sales Module
1. Study: Account + Project (shared with Finance)
2. Study: AccountDashboard + DeliveryUnit
3. Study: Sales services (72 nodes)

### Understanding AI/Document Processing
1. Study: LlamaCloudDocumentParser (31 edges)
2. Study: Document Processing community (38 nodes)
3. Study: AI Engine community (18 nodes)

### Understanding Integration
1. Study: Account + Project (god nodes)
2. Study: integration-guide.md (data flows)
3. Study: Doc Insighter as SHARED engine

---

## 🔗 Related Documents

- [PATTERNS.md](PATTERNS.md) — Code patterns & conventions
- [integration-guide.md](integration-guide.md) — Cross-module data flows
- [PROJECT_CONTEXT.md](../../PROJECT_CONTEXT.md) — Project context & tech stack
- `graphify-out/graph.json` — Full Graphify analysis (raw data)
- `graphify-out/GRAPH_REPORT.md` — Full Graphify report

---

## ✅ Quick Checklist for Impact Analysis

**Before making changes, ask:**

1. ✅ Is this a god node? (Account, Project, Logger, RevenueMaster, LlamaCloudDocumentParser)
   - If YES → HIGH risk, coordinate with multiple teams
   
2. ✅ Does this affect Account or Project?
   - If YES → Affects Finance + Sales, test both
   
3. ✅ Does this affect Logger?
   - If YES → CRITICAL risk, minimal changes only
   
4. ✅ Is this cross-module (Finance ↔ Sales)?
   - If YES → Test integration, regression suite needed
   
5. ✅ Does this affect Doc Insighter?
   - If YES → Test all extraction workflows

---

**Generated by Graphify on 2026-05-06 | Updated 2026-05-07**
