# Cross-Module Integration Guide

Document data flows, dependencies, and integration patterns between Finance, Sales, Doc Insighter, and Insights Workflow modules.

---

## 📊 ARCHITECTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND / APIs                       │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐      ┌──────────────┐    ┌──────────────┐
│   FINANCE    │      │    SALES     │    │ DOC_INSIGHTER│
│    MODULE    │      │    MODULE    │    │  (SHARED)    │
├──────────────┤      ├──────────────┤    ├──────────────┤
│ • Accounts   │      │ • Dashboards │    │ • Extraction │
│ • Projects   │      │ • Calendars  │    │ • LlamaParse │
│ • Revenue    │      │ • Stakeholder│    │ • CrewAI     │
│ • Budgets    │      │ • Allocation │    │   Orchestr.  │
│ • KPIs       │      │ • Insights   │    │ • Prompts    │
└──────────────┘      └──────────────┘    └──────────────┘
        │                   │                      ▲
        │ Documents         │ Documents            │
        │ (uploads)         │ (uploads)            │
        ├───────────────────┴────────────────────┬─┘
        │        finance/doc_processor            │
        │        sales/doc_processor              │
        │                                         │
        └─────────────────►  DOC ANALYSIS  ◄──────┘
                            (LlamaParse)
                                │
                                ▼
                        ┌──────────────────┐
                        │  INSIGHTS_       │
                        │  WORKFLOW        │
                        ├──────────────────┤
                        │ • Aggregation    │
                        │ • Multi-agent    │
                        │   analysis       │
                        │ • S3 staging     │
                        │ • Async results  │
                        └──────────────────┘
                                │
                        ┌───────┼───────┐
                        ▼       ▼       ▼
                    PostgreSQL S3     Cache
```

---

## 🔀 DATA FLOWS

### Flow 1: Document Upload → Extraction → Storage

**Path:** Finance/Sales API → Document Processor → Doc Insighter → PostgreSQL + S3

```yaml
trigger: "POST /api/v1/{finance|sales}/documents"
input: "File upload (SOW, WSR, code review, etc.)"
steps:
  1. Document Processor stores to S3: "s3://project-insighter/uploads/{organization_id}/{doc_type}/"
  2. Calls Doc Insighter with:
     - s3_path: "s3://..../file.pdf"
     - doc_type: "SOW" | "WSR" | "code_review" | "best_practices"
     - context: {account_id, project_id, organization_id}
  3. Doc Insighter:
     - Calls LlamaParse to extract text/tables/metadata
     - Runs CrewAI crew (role-based agents per doc_type)
     - Returns structured JSON (KPIs, insights, confidence scores)
  4. Document Processor stores parsed result:
     - postgres: ProjectDocument table
     - s3: "s3://project-insighter/parsed/{doc_id}/kpis.json"
output: "DocumentProcessingResult {document_id, kpis, insights, confidence}"
```

**Code References:**
- Upload: `backend/finance/app/api/import_data.py` → `import_and_save_file()`
- Extract: `backend/doc_insighter/core/extraction_pipeline.py` → `extract_kpis()`
- Store: `backend/finance/doc_processor/services/best_practices.py` → `process_best_practices_document()`

---

### Flow 2: Account/Project CRUD with Cross-Module Updates

**Path:** Finance API → PostgreSQL → (triggers) Sales Service for Dashboard Sync

```yaml
trigger: "POST|PUT /api/v1/finance/accounts"
input: "Account {name, organization_id, revenue_tier, contact_info}"
steps:
  1. Finance Service validates & persists Account to PostgreSQL
  2. Publishes event: "account_created" | "account_updated"
  3. Sales Module listens (optional - currently manual):
     - Optionally creates AccountDashboard entry
     - Links to existing Stakeholders
  4. Returns Account response
output: "AccountOut {id, name, organization_id, created_at}"

cross_module_risk: "Account model is shared (not replicated)"
  - Single source of truth in PostgreSQL
  - Both modules query same Account table
  - NO data consistency issues (ACID guaranteed)
```

**Code References:**
- Finance: `backend/finance/app/api/account.py` → CRUD endpoints
- Sales: `backend/sales/app/models/account_dashboard.py` → Links to Account via account_id FK

---

### Flow 3: Insights Generation (Aggregated)

**Path:** Insights Workflow → Multiple Analysis Crews → S3 Staging → Results

```yaml
trigger: "POST /api/v1/insights/generate"
input: "InsightRequest {account_id, project_id, analysis_types}"
steps:
  1. Insights Workflow loads context from PostgreSQL:
     - Account details
     - Project details
     - Associated documents (Finance + Sales)
     - Historical revenue/budget data
  2. Stages raw data to S3: "s3://project-insighter/staging/{job_id}/"
  3. Runs multi-agent crews in parallel:
     - Finance Analyzer Crew (revenue trends, KPI analysis)
     - Risk Analyzer Crew (from WSR/SOW documents)
     - Team Allocation Crew (from Sales allocation data)
  4. Aggregates results: "s3://project-insighter/results/{job_id}/insights.json"
  5. Returns 202 Accepted with job_id for async polling
output: "InsightGenerationResponse {job_id, status, estimated_completion}"

async_pattern: "Client polls GET /api/v1/insights/{job_id} for status/results"
```

**Code References:**
- Orchestration: `backend/insights_workflow/core/generalized_crew.py`
- Services: `backend/insights_workflow/services/finance_insights_service.py`
- Async API: `backend/insights_workflow/api/insights.py`

---

## 🗂️ SHARED DATA MODELS

### Account (Shared across Finance & Sales)

```yaml
model: Account
source_of_truth: PostgreSQL (Supabase)
accessed_by: [Finance Module, Sales Module, Insights Workflow]
relationships:
  - Project (1:N)
  - AccountDashboard (1:1, Sales-specific)
  - Document (1:N, Finance/Sales docs)
  - Revenue (1:N, Finance-specific)
  - DeliveryUnit (M:N via AccountDeliveryUnit junction)
```

**Implications:**
- Changes in Finance Account must be visible immediately to Sales
- Account deletion cascades to all related Projects, Documents, Insights
- NO separate Account table per module (single source of truth)

---

### Document (Shared Processor)

```yaml
entity: ProjectDocument | AccountDocument
storage: PostgreSQL + S3
processors: [LlamaParse (extraction), CrewAI (analysis)]
doc_types:
  - SOW (Statement of Work) → Finance processor
  - WSR (Weekly Status Report) → Sales processor
  - Code Review → Finance or Sales processor
  - Best Practices → Finance or Sales processor
output_structure:
  s3_path: "s3://project-insighter/parsed/{doc_id}/kpis.json"
  postgres_table: ProjectDocument | AccountDocument
  fields: {extracted_text, kpis, confidence, created_at, updated_at}
```

---

### PostgreSQL Foreign Key Dependencies

```sql
-- Cross-module relationships
Account (id) ← Project.account_id
Account (id) ← AccountDashboard.account_id
Account (id) ← AccountDocument.account_id

Project (id) ← ProjectDocument.project_id
Project (id) ← Revenue.project_id
Project (id) ← DeliveryUnitProject.project_id

-- Implications for deletion:
ON DELETE CASCADE from Account:
  - Projects deleted
  - Documents deleted
  - Dashboards deleted
  - Revenues deleted

-- Test with: SELECT constraint_name FROM information_schema.table_constraints WHERE table_name='Account'
```

---

## 🔌 INTEGRATION PATTERNS

### Pattern 1: Service-to-Service Calls (Synchronous)

**When:** Finance API needs to fetch Sales allocation data

```python
# finance/app/services/project.py
from backend.sales.app.services.account_dashboard_service import AccountDashboardService

class ProjectService:
    def get_project_with_sales_context(self, project_id):
        project = db.query(Project).get(project_id)
        
        # Call Sales service for dashboard context
        sales_service = AccountDashboardService(db)
        dashboard = sales_service.get_by_account_id(project.account_id)
        
        return {
            "project": project,
            "sales_allocation": dashboard.allocation_data
        }
```

**Risk:** Tight coupling if service is slow (timeout)  
**Mitigation:** Cache dashboard data, set timeouts, handle failures gracefully

---

### Pattern 2: Event-Driven (Asynchronous)

**When:** Account update should optionally trigger Sales dashboard refresh

```python
# finance/app/services/account.py
import asyncio

class AccountService:
    def update_account(self, account_id, update_data):
        account = db.query(Account).get(account_id)
        account.update(update_data)
        db.commit()
        
        # Async event: Sales module can listen (currently manual)
        asyncio.create_task(self._publish_account_updated_event(account_id))
        
        return account
    
    async def _publish_account_updated_event(self, account_id):
        logger.info(f"Account {account_id} updated - Sales team notified")
        # Future: Kafka/RabbitMQ pub/sub integration
```

**Benefit:** Decoupled modules, async processing  
**Limitation:** Currently single-process (no queue), need distributed event system for scalability

---

### Pattern 3: Shared AI Engine (Doc Insighter)

**Both Finance & Sales call Doc Insighter for document processing:**

```python
# finance/doc_processor/services/sow.py
from backend.doc_insighter.core.extraction_pipeline import extract_kpis

class SOWProcessor:
    def process_sow_document(self, s3_path, account_id):
        # Call shared Doc Insighter engine
        kpis = extract_kpis(
            s3_path=s3_path,
            doc_type="SOW",
            context={"account_id": account_id}
        )
        # Store results
        self._save_kpis_to_db(account_id, kpis)
        return kpis

# sales/doc_processor/services/wsr.py
from backend.doc_insighter.core.extraction_pipeline import extract_kpis

class WSRProcessor:
    def process_wsr_document(self, s3_path, account_id):
        # Same engine, different doc_type
        kpis = extract_kpis(
            s3_path=s3_path,
            doc_type="WSR",
            context={"account_id": account_id}
        )
        self._save_kpis_to_db(account_id, kpis)
        return kpis
```

**Benefit:** Single source of truth for document extraction  
**Responsibility:** Doc Insighter must be stateless and reusable

---

## ⚠️ INTEGRATION RISKS & MITIGATIONS

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Account deletion cascades too broad** | Loss of Sales data | Add soft delete (deleted_at timestamp) + cascade tests |
| **Slow Doc Insighter call blocks API** | Timeout errors | Make document processing async (202 Accepted) + callback |
| **Finance/Sales queries N+1 on Account** | Performance degrade | Use materialized view (AccountMetricsMV) + caching |
| **Insights Workflow stale data** | Incorrect analysis | Refresh cache on Account/Project update (event trigger) |
| **Cross-module bug affects both modules** | Data integrity risk | Comprehensive integration tests (test_account_sync.py) |
| **S3 upload fails during extraction** | Partial state in DB | Idempotent document processing + retry logic |

---

## 🧪 INTEGRATION TESTING STRATEGY

### Test Suite: `tests/integration/test_cross_module.py`

```python
# Scenario 1: Account creation propagates to Sales
def test_account_created_visible_in_sales():
    account = create_finance_account(name="Acme Corp")
    assert account.id in db.query(Account).all()
    
    # Sales service should see it
    dashboard = create_sales_dashboard(account_id=account.id)
    assert dashboard.account_id == account.id

# Scenario 2: Document upload triggers extraction in both modules
def test_document_upload_extraction():
    account = create_finance_account()
    doc_response = upload_sow_document(account_id=account.id)
    
    # Check Finance processor picked it up
    docs = db.query(ProjectDocument).filter_by(account_id=account.id).all()
    assert len(docs) > 0
    assert docs[0].extracted_text is not None

# Scenario 3: Insights workflow aggregates Finance + Sales data
def test_insights_workflow_aggregation():
    account = create_account()
    project = create_project(account_id=account.id)
    upload_sow_document(project_id=project.id)
    upload_wsr_document(account_id=account.id)
    
    insights = generate_insights(account_id=account.id)
    assert insights.finance_metrics is not None
    assert insights.sales_context is not None
    assert insights.document_insights is not None
```

---

## 📋 CHECKLIST FOR NEW CROSS-MODULE FEATURES

- [ ] Entity requires foreign key to Account/Project? → Use shared model (don't replicate)
- [ ] Feature needs document processing? → Route through Doc Insighter (not separate)
- [ ] Feature needs insights generation? → Coordinate with Insights Workflow
- [ ] Data impacts both Finance & Sales? → Add integration test
- [ ] Deletion cascades? → Document CASCADE behavior, test rollback
- [ ] API change affects other module? → Notify and coordinate deprecation
- [ ] Adding new doc_type? → Register in Document Processor, update CrewAI prompts

---

**Version:** 1.0 | **Last Updated:** 2026-05-07
