# Project Insighter Backend

A sophisticated FastAPI-based enterprise backend for **project management**, **financial tracking**, **sales pipeline management**, and **AI-driven document analysis**. The system leverages **Azure OpenAI**, **CrewAI**, and **LlamaParse** for intelligent document extraction and multi-agent insight generation, deployed on **AWS Lambda** via Docker container images pushed to **ECR**.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Tech Stack](#tech-stack)
4. [Core Modules](#core-modules)
   - [Finance Module](#finance-module)
   - [Sales Module](#sales-module)
   - [Insights Workflow Module](#insights-workflow-module)
   - [Doc Insighter AI Engine](#doc-insighter-ai-engine)
   - [AI Insighter Engine](#ai-insighter-engine)
5. [API Endpoints Reference](#api-endpoints-reference)
   - [Health Check](#health-check-1-endpoint)
6. [Database Schema](#database-schema)
7. [Service Layer Architecture](#service-layer-architecture)
8. [Document Processing Pipeline](#document-processing-pipeline)
9. [Insight Generation Flow](#insight-generation-flow)
10. [S3 Storage Layout](#s3-storage-layout)
11. [Environment Variables](#environment-variables)
12. [Local Development](#local-development)
13. [Docker Deployment](#docker-deployment)

---

## Architecture Overview

```
                         ┌─────────────────┐
                         │   CloudFront    │
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  API Gateway    │
                         └────────┬────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │    AWS Lambda (Docker)     │
                    │   FastAPI + Mangum         │
                    └─┬──────────┬──────────┬────┘
                      │          │          │
        ┌─────────────┴┐  ┌──────┴─────┐  ┌┴──────────────┐
        │ PostgreSQL   │  │   AWS S3    │  │ Azure OpenAI  │
        │ (Supabase)   │  │  (Uploads)  │  │   (GPT-4o)    │
        └──────────────┘  └──────┬──────┘  └───────────────┘
                                 │
                        ┌────────▼────────┐
                        │  LlamaParse API │
                        │  (Document Ext) │
                        └─────────────────┘

    ┌──────────────────────────────────────────────────┐
    │          BACKEND APPLICATION LAYERS              │
    ├──────────────────────────────────────────────────┤
    │  API Layer (FastAPI routes + schemas)            │
    │  Service Layer (Business logic + orchestration)  │
    │  AI Engine (CrewAI multi-agent orchestration)    │
    │  Data Layer (SQLAlchemy ORM + PostgreSQL)        │
    │  Storage Layer (S3 + file management)            │
    └──────────────────────────────────────────────────┘
```

**Key Data Flows:**
- **Finance & Sales Modules** → Document uploads → **Doc Insighter Engine** → LlamaParse extraction → CrewAI analysis → PostgreSQL storage + S3
- **Insights Workflow** → Multi-agent async generation → Document aggregation → Stored insights (async, 202 Accepted pattern)
- **Calendar System** → Time-based events, milestones, reminders for Sales stakeholder management
- **Data Export** → PostgreSQL → Excel/CSV export endpoints

---

## Project Structure

```
project-insighter-backend/
├── main.py                          # FastAPI app entry point + Mangum Lambda handler
├── pyproject.toml                   # uv-based dependencies & build config
├── Dockerfile                       # AWS Lambda Python 3.12 image
├── docker-compose.yml               # Local Docker Compose setup
├── readme.md                        # This file
│
├── backend/
│   ├── core/
│   │   └── config.py                # BaseSettings, DATABASE_URL, environment config
│   │
│   ├── db/
│   │   ├── base.py                  # SQLAlchemy declarative Base
│   │   ├── session.py               # Engine, SessionLocal, get_db() dependency
│   │   └── __init__.py
│   │
│   ├── doc_insighter/               # ⭐ SHARED AI DOCUMENT ANALYSIS ENGINE
│   │   ├── core/
│   │   │   ├── ai_agent.py          # CrewAI orchestration + agent definitions
│   │   │   ├── extraction_pipeline.py # Document → structured KPI extraction
│   │   │   ├── insight_agents.py    # Multi-agent SOW/WSR/Code Quality analysis
│   │   │   ├── document_kpi_prompts.py # Prompt templates per document type
│   │   │   ├── llama_parsing.py     # LlamaParse API integration
│   │   │   ├── json_to_markdown.py  # Structured JSON → readable markdown
│   │   │   └── __init__.py
│   │   │
│   │   └── tools/
│   │       ├── app_logger.py        # Loguru-based application logger
│   │       ├── file_reader_tool.py  # CrewAI file reader tool
│   │       ├── llama_tool.py        # LlamaIndex query tool for parsed docs
│   │       ├── llm_models.py        # Azure OpenAI model configuration
│   │       ├── store_data.py        # Data persistence tool for agents
│   │       └── __init__.py
│   │
│   ├── ai_insighter/                # Additional AI capabilities
│   │   ├── engine/
│   │   │   ├── config.py            # Engine-specific configuration
│   │   │   ├── pipeline.py          # AI processing pipeline
│   │   │   └── __init__.py
│   │   │
│   │   └── services/
│   │       ├── project_insighter.py # Core insight generation logic
│   │       ├── prompts.py           # Additional prompt templates
│   │       └── __init__.py
│   │
│   ├── insights_workflow/           # ⭐ ASYNC INSIGHT GENERATION SYSTEM
│   │   ├── api/
│   │   │   ├── insights.py          # 6 insight endpoints (project/account/PE)
│   │   │   └── __init__.py
│   │   │
│   │   ├── core/
│   │   │   ├── context_aware_agents.py # Agent configuration per entity type
│   │   │   ├── generalized_crew.py  # Generalized CrewAI multi-agent setup
│   │   │   └── __init__.py
│   │   │
│   │   ├── services/
│   │   │   ├── finance_insights_service.py # Finance insight generation
│   │   │   ├── finance_aggregation_service.py # Cross-document aggregation
│   │   │   ├── json_transformer.py  # Data transformation utility
│   │   │   └── __init__.py
│   │   │
│   │   ├── tools/
│   │   ├── utilities/
│   │   └── __init__.py
│   │
│   ├── sales/                       # SALES PIPELINE & ACCOUNT MANAGEMENT
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── account_dashboard.py   # Account dashboard CRUD
│   │   │   │   ├── stakeholder_details.py # Stakeholder contact mgmt
│   │   │   │   ├── calendar_task.py       # Task management
│   │   │   │   ├── calendar_milestone.py  # Milestone management
│   │   │   │   ├── calendar_reminder.py   # Reminder management
│   │   │   │   ├── calendar_event.py      # Calendar event view
│   │   │   │   ├── export_data.py         # Data export endpoints
│   │   │   │   ├── deps.py                # FastAPI dependencies
│   │   │   │   └── __init__.py
│   │   │   │
│   │   │   ├── models/
│   │   │   │   ├── account_dashboard.py
│   │   │   │   ├── stakeholder_details.py
│   │   │   │   ├── calendar_task.py
│   │   │   │   ├── calendar_milestone.py
│   │   │   │   ├── calendar_reminder.py
│   │   │   │   ├── calendar_reminder_users.py
│   │   │   │   ├── calendar_event.py
│   │   │   │   ├── document.py
│   │   │   │   └── __init__.py
│   │   │   │
│   │   │   ├── schemas/             # Pydantic request/response schemas
│   │   │   │
│   │   │   └── services/
│   │   │       ├── account_dashboard_service.py
│   │   │       ├── stakeholder_details_service.py
│   │   │       ├── calendar_task_service.py
│   │   │       ├── calendar_milestone_service.py
│   │   │       ├── calendar_reminder_service.py
│   │   │       ├── calendar_event_service.py
│   │   │       ├── export_service.py
│   │   │       └── __init__.py
│   │   │
│   │   └── doc_processor/           # SALES DOCUMENT ANALYSIS
│   │       ├── api/
│   │       │   ├── sow.py                 # SOW import/retrieve/delete
│   │       │   ├── wsr.py                 # WSR import/retrieve/delete
│   │       │   ├── code_quality.py        # Code quality import/retrieve/delete
│   │       │   ├── tech_review.py         # Tech review import/retrieve/delete
│   │       │   ├── best_practices.py      # Best practices import/retrieve/delete
│   │       │   ├── project_docs.py        # File list/download/delete
│   │       │   ├── insights.py            # Circle allocation insights
│   │       │   └── __init__.py
│   │       │
│   │       └── services/
│   │           ├── sow.py
│   │           ├── wsr.py
│   │           ├── code_quality.py
│   │           ├── tech_review.py
│   │           ├── best_practices.py
│   │           ├── insight_service.py     # Circle allocation logic
│   │           ├── project_file_service.py # S3 file management
│   │           └── __init__.py
│   │
│   ├── finance/                     # FINANCE & PROJECT ACCOUNTING
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── account.py             # Account CRUD + refresh-metrics
│   │   │   │   ├── project.py             # Project CRUD
│   │   │   │   ├── delivery_unit.py       # Delivery unit CRUD
│   │   │   │   ├── dashboard.py           # Financial dashboard endpoints
│   │   │   │   ├── import_data.py         # Bulk data import
│   │   │   │   ├── export_data.py         # Data export
│   │   │   │   ├── private_equity.py      # Private equity CRUD
│   │   │   │   ├── pmo_docs.py            # PMO file endpoints
│   │   │   │   └── __init__.py
│   │   │   │
│   │   │   ├── models/
│   │   │   │   ├── account.py             # Finance account model
│   │   │   │   ├── project.py             # Finance project model
│   │   │   │   ├── delivery_unit.py       # Organizational delivery unit
│   │   │   │   ├── private_equity.py      # PE record model
│   │   │   │   ├── private_equity_document.py # PE doc tracking
│   │   │   │   ├── document.py            # Finance doc model
│   │   │   │   ├── revenue.py             # Revenue tracking model
│   │   │   │   └── __init__.py
│   │   │   │
│   │   │   ├── schemas/             # Pydantic request/response schemas
│   │   │   │
│   │   │   └── services/
│   │   │       ├── account.py
│   │   │       ├── project.py
│   │   │       ├── delivery_unit.py
│   │   │       ├── private_equity.py
│   │   │       ├── revenue.py
│   │   │       ├── dashboard_services.py
│   │   │       ├── import_service.py
│   │   │       ├── export_services.py
│   │   │       ├── file_scanner.py
│   │   │       └── __init__.py
│   │   │
│   │   └── doc_processor/           # FINANCE DOCUMENT ANALYSIS
│   │       ├── api/
│   │       │   ├── sow.py                 # SOW import/retrieve/delete
│   │       │   ├── wsr.py                 # WSR import/retrieve/delete
│   │       │   ├── code_quality.py        # Code quality analysis
│   │       │   ├── tech_review.py         # Tech review analysis
│   │       │   ├── best_practices.py      # Best practices analysis
│   │       │   ├── project_docs.py        # File management
│   │       │   ├── private_equity_docs.py # PE-specific document endpoints
│   │       │   └── __init__.py
│   │       │
│   │       └── services/
│   │           ├── sow.py
│   │           ├── wsr.py
│   │           ├── code_quality.py
│   │           ├── tech_review.py
│   │           ├── best_practices.py
│   │           ├── private_equity_docs.py
│   │           └── project_file_service.py
│   │
│   └── utitlites/                   # ⚠️ SHARED UTILITIES (note: folder typo in codebase)
│       ├── __init__.py
│       ├── app_utilites.py          # safe_float, safe_int, type conversion helpers
│       ├── async_pool_executor.py   # ThreadPoolExecutor for sync-in-async patterns
│       ├── doc_importer.py          # File upload → S3 → processing pipeline
│       ├── s3_storage.py            # S3 client wrapper + upload/download/delete
│       └── llm_models.py            # LLM model configuration & constants
│
├── graphify-out/                    # Auto-generated documentation outputs
│   ├── graph.html                   # Interactive knowledge graph
│   ├── graph.json                   # Graph data structure
│   ├── GRAPH_REPORT.md              # Analysis report
│   ├── cost.json                    # Processing cost tracking
│   └── cache/                       # Processing cache

```

**Module Responsibilities:**

| Module | Purpose | Key Entities |
|--------|---------|--------------|
| **Finance** | Project accounting, revenue tracking, financial reporting | Accounts, Projects, Delivery Units, Revenue, Private Equity |
| **Sales** | Sales pipeline, account management, stakeholder tracking | Account Dashboards, Stakeholders, Calendar (Tasks/Milestones/Reminders) |
| **Insights Workflow** | Async insight generation via multi-agent CrewAI | Project/Account/PE insights, aggregation, storage |
| **Doc Insighter** | Shared AI-powered document extraction & analysis | LlamaParse integration, CrewAI agents, KPI extraction |
| **AI Insighter** | Additional AI capabilities | Insight logic, prompt engineering |
| **Utilities** | Shared infrastructure | S3 storage, document importing, type helpers, async patterns |

---

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Framework** | FastAPI | 0.128.1 |
| **ASGI Server** | Uvicorn | 0.40.0 |
| **Lambda Adapter** | Mangum | 0.21.0 |
| **Python** | Python | 3.12+ |
| **ORM** | SQLAlchemy | 2.0.46 |
| **Database** | PostgreSQL (Supabase) | 15+ |
| **DB Driver** | Psycopg2 | Latest |
| **Validation** | Pydantic | 2.12.5 |
| **Settings** | pydantic-settings | 2.12.0 |
| **AI/LLM** | Azure OpenAI | Latest |
| **Document Extraction** | LlamaCloud (LlamaParse) | 0.6.94 |
| **Vector/RAG** | LlamaIndex | Latest |
| **Multi-Agent Orchestration** | CrewAI | 1.6.1 |
| **Cloud Storage** | AWS S3 (Boto3) | 1.35.0 |
| **Data Processing** | Pandas | 3.0.0 |
| **Logging** | Loguru | 0.7.3 |
| **Fuzzy Matching** | RapidFuzz | 3.14.3 |
| **Package Manager** | uv | Latest |
| **Container Runtime** | Docker | Latest |

---

## Core Modules

### Finance Module

**Overview:** Comprehensive financial management system for project accounting, budgeting, revenue tracking, and financial reporting.

#### Finance API Endpoints

**Accounts** (`/api/v1/accounts`)
- `GET /` — List all accounts with pagination
- `POST /` — Create new account (201)
- `GET /{account_id}` — Get single account
- `PUT /{account_id}` — Update account
- `DELETE /{account_id}` — Delete account (200)
- `POST /refresh-account-metrics` — Recalculate account metrics

**Projects** (`/api/v1/projects`)
- `GET /` — List all projects with pagination
- `POST /` — Create new project (201)
- `GET /account/{account_id}` — List projects by account
- `GET /{project_id}` — Get single project
- `PUT /{project_id}` — Update project
- `DELETE /{project_id}` — Delete project (200)

**Delivery Units** (`/api/v1/delivery_units`)
- `GET /` — List all delivery units

**Private Equity** (`/api/v1/finance/private-equity`)
- `POST /` — Create PE record (201)
- `GET /` — List PE records
- `GET /{pe_id}` — Get single PE record
- `PUT /{pe_id}` — Update PE record
- `DELETE /{pe_id}` — Delete PE record (204)

**Dashboard & Analytics** (`/api/v1/dashboard`)
- `POST /` — Create dashboard data
- `GET /get_data` — Get dashboard data
- `GET /account_summary` — Get account revenue summary

**Data Import/Export** (`/api/v1/import`, `/api/v1/export`)
- `POST /import/project` — Import project data
- `POST /import/revenue` — Import revenue data
- `GET /export/all_projects` — Export all projects
- `GET /export/all_revenues` — Export all revenues

**PMO Documents** (`/api/v1/pmo`)
- `GET /pmo-files` — List PMO files
- `GET /revenue-files` — List revenue files

#### Finance Document Processor (5 Document Types)

**SOW Documents** (`/api/v1/finance/document/import_sow`)
- `POST /import_sow/{project_id}` — Upload SOW document
- `GET /sow/{project_id}` — Retrieve SOW with extracted data
- `DELETE /sow/{project_id}` — Delete SOW document

**WSR Documents** (`/api/v1/finance/document/import_wsr`)
- `POST /import_wsr/{project_id}` — Upload WSR document
- `GET /wsr/{project_id}` — Retrieve WSR with extracted data
- `DELETE /wsr/{project_id}` — Delete WSR document

**Code Quality Documents**
- `POST /import_code_quality/{project_id}` — Upload code quality report
- `GET /code_quality/{project_id}` — Retrieve code quality analysis
- `DELETE /code_quality/{project_id}` — Delete code quality doc

**Tech Review Documents**
- `POST /import_tech_review/{project_id}` — Upload tech review
- `GET /tech_review/{project_id}` — Retrieve tech review analysis
- `DELETE /tech_review/{project_id}` — Delete tech review doc

**Best Practices Documents**
- `POST /import_best_practices/{project_id}` — Upload best practices
- `GET /best_practices/{project_id}` — Retrieve best practices analysis
- `DELETE /best_practices/{project_id}` — Delete best practices doc

**Project Document Management** (`/api/v1/finance/document`)
- `GET /list/{project_id}/{category}` — List files by category (sow, wsr, code_quality, tech_review, best_practices)
- `GET /download/{project_id}/{filename}` — Download file (S3 presigned URL)
- `DELETE /delete/{project_id}/{filename}` — Delete file from S3

**Private Equity Documents** (`/api/v1/finance`)
- `POST /import/{pe_id}/{document_type}` — Upload PE document (Company Capabilities, PE Details, etc.)
- `GET /{pe_id}/{document_type}` — Retrieve PE document with extracted data
- `DELETE /{pe_id}/{document_type}` — Delete PE document

#### Finance Database Models

| Model | Key Fields | Relationships |
|-------|-----------|---------------|
| **Account** | id, name, code, account_status, created_at, updated_at | ← Projects, Documents |
| **Project** | id, account_id (FK), project_name, start_date, end_date, budget, status | → Account, ← Documents, ← Revenue |
| **DeliveryUnit** | id, name, manager_id | |
| **PrivateEquity** | id, pe_name, status, created_at, updated_at | ← PrivateEquityDocuments |
| **PrivateEquityDocument** | id, pe_id (FK), document_type, s3_key, metadata, uploaded_at | → PrivateEquity |
| **Document** | id, project_id (FK), doc_type, s3_key, uploaded_at, extracted_insights (JSONB) | → Project |
| **Revenue** | id, project_id (FK), amount, date, category | → Project |

#### Finance Services (10 services)

| Service | Key Methods | Responsibilities |
|---------|------------|------------------|
| **AccountService** | create, get, update, delete, list, refresh_metrics | Account CRUD, metric calculation |
| **ProjectService** | create, get, update, delete, list_by_account, calculate_kpis | Project CRUD, KPI calculation |
| **DeliveryUnitService** | get, list | Delivery unit retrieval |
| **PrivateEquityService** | create, get, update, delete, list | PE CRUD operations |
| **RevenueService** | create, import_bulk, export_all, calculate_totals | Revenue tracking & aggregation |
| **DashboardService** | get_dashboard_data, account_summary, project_metrics | Dashboard data aggregation |
| **ImportService** | import_projects, import_revenue | Bulk data import |
| **ExportService** | export_projects, export_revenue | Data export (Excel/CSV) |
| **FileScanner** | scan_s3, validate_files, process_batches | S3 file scanning & validation |
| **ProjectFileService** | upload, download, delete, list, generate_presigned_urls | S3 file lifecycle management |

---

### Sales Module

**Overview:** Sales pipeline management with account dashboards, stakeholder tracking, calendar-based planning, and AI-driven team allocation insights.

#### Sales API Endpoints

**Account Dashboard** (`/api/v1/account-dashboard`)
- `POST /` — Create account dashboard (201)
- `GET /` — List all account dashboards
- `GET /{account_id}` — Get single account dashboard
- `PUT /{account_id}` — Update account dashboard
- `DELETE /{account_id}` — Delete account dashboard (204)

**Stakeholder Details** (`/api/v1/stakeholder-details`)
- `POST /` — Create stakeholder (201)
- `GET /` — List all stakeholders
- `GET /{stakeholder_id}` — Get single stakeholder
- `GET /account/{account_id}` — List stakeholders by account
- `PUT /{stakeholder_id}` — Update stakeholder
- `DELETE /{stakeholder_id}` — Delete stakeholder (204)
- `GET /search/incumbency/{strength}` — Search stakeholders by incumbency strength

**Calendar Tasks** (`/api/v1/calendar/tasks`)
- `POST /` — Create task (201)
- `PUT /{task_id}` — Update task
- `DELETE /{task_id}` — Delete task (204)

**Calendar Milestones** (`/api/v1/calendar/milestones`)
- `POST /` — Create milestone (201)
- `PUT /{milestone_id}` — Update milestone
- `DELETE /{milestone_id}` — Delete milestone (204)

**Calendar Reminders** (`/api/v1/calendar/reminders`)
- `POST /` — Create reminder (201)
- `PUT /{reminder_id}` — Update reminder
- `DELETE /{reminder_id}` — Delete reminder (204)

**Calendar Events** (`/api/v1/calendar/events`)
- `GET /` — List calendar events (aggregated view)

**Sales Document Processor** (5 Document Types)

**SOW** (`/api/v1/document/import_sow`)
- `POST /import_sow/{account_id}` — Upload SOW document
- `GET /sow/{account_id}` — Retrieve SOW analysis
- `DELETE /sow/{account_id}` — Delete SOW document

**WSR** (`/api/v1/document/import_wsr`)
- `POST /import_wsr/{account_id}` — Upload WSR document
- `GET /wsr/{account_id}` — Retrieve WSR analysis
- `DELETE /wsr/{account_id}` — Delete WSR document

**Code Quality** (`/api/v1/document/import_code_quality`)
- `POST /import_code_quality/{account_id}` — Upload code quality report
- `GET /code_quality/{account_id}` — Retrieve code quality analysis
- `DELETE /code_quality/{account_id}` — Delete code quality doc

**Tech Review** (`/api/v1/document/import_tech_review`)
- `POST /import_tech_review/{account_id}` — Upload tech review
- `GET /tech_review/{account_id}` — Retrieve tech review analysis
- `DELETE /tech_review/{account_id}` — Delete tech review doc

**Best Practices** (`/api/v1/document/import_best_practices`)
- `POST /import_best_practices/{account_id}` — Upload best practices
- `GET /best_practices/{account_id}` — Retrieve best practices analysis
- `DELETE /best_practices/{account_id}` — Delete best practices doc

**Document Management** (`/api/v1/document`)
- `GET /list/{project_id}/{category}` — List files by category
- `GET /download/{project_id}/{filename}` — Download file (S3 presigned URL)
- `DELETE /delete/{project_id}/{filename}` — Delete file

**Sales Insights** (`/api/v1/insights`)
- `POST /circle-allocation/{project_id}` — Generate circle/team allocation insights

**Sales Export** (`/api/v1/export`)
- `GET /accounts` — Export accounts data
- `GET /stakeholders` — Export stakeholders data

#### Sales Database Models

| Model | Key Fields | Relationships |
|-------|-----------|---------------|
| **AccountDashboard** | id, account_id, pipeline_value, win_probability, last_updated | |
| **StakeholderDetails** | id, account_id (FK), name, email, role, incumbency_strength | → Account |
| **CalendarTask** | id, project_id (FK), title, description, due_date, status, priority | → Project |
| **CalendarMilestone** | id, project_id (FK), name, target_date, status | → Project |
| **CalendarReminder** | id, milestone_id (FK), reminder_date, message | → Milestone, ← CalendarReminderUsers |
| **CalendarReminderUsers** | id, reminder_id (FK), user_id | → Reminder |
| **CalendarEvent** | Aggregated view of tasks, milestones, reminders | |
| **Document** | id, account_id (FK), doc_type, s3_key, uploaded_at, extracted_insights (JSONB) | → Account |

#### Sales Services (8 services)

| Service | Key Methods | Responsibilities |
|---------|------------|------------------|
| **AccountDashboardService** | create, get, update, delete, list | Dashboard CRUD |
| **StakeholderDetailsService** | create, get, update, delete, list, search_by_incumbency | Stakeholder management |
| **CalendarTaskService** | create, update, delete, list | Task management |
| **CalendarMilestoneService** | create, update, delete, list | Milestone management |
| **CalendarReminderService** | create, update, delete, list | Reminder management |
| **CalendarEventService** | get_events, aggregate_calendar | Calendar view generation |
| **ExportService** | export_accounts, export_stakeholders | Data export |
| **ProjectFileService** | upload, download, delete, list, generate_presigned_urls | S3 file lifecycle |

---

### Insights Workflow Module

**Overview:** Asynchronous insight generation for Finance projects, Sales accounts, and Private Equity records using multi-agent CrewAI orchestration.

#### Insights Workflow API Endpoints

**Project Insights** (`/api/v1/insights`)
- `POST /project/{project_id}` — Trigger project insight generation (202 Accepted)
- `GET /project/{project_id}` — Retrieve stored project insights

**Account Insights** (`/api/v1/insights`)
- `POST /account/{account_id}` — Trigger account insight generation (202 Accepted)
- `GET /account/{account_id}` — Retrieve stored account insights

**Private Equity Insights** (`/api/v1/insights`)
- `POST /pe/{pe_id}` — Trigger PE insight generation (202 Accepted)
- `GET /pe/{pe_id}` — Retrieve stored PE insights

#### Insights Workflow Architecture

- **GeneralizedCrew** (`generalized_crew.py`): Multi-agent CrewAI orchestration engine
- **ContextAwareAgents** (`context_aware_agents.py`): Dynamic agent configuration based on entity type
- **FinanceInsightsService** (`finance_insights_service.py`): Finance-specific insight generation
- **FinanceAggregationService** (`finance_aggregation_service.py`): Cross-document aggregation logic
- **JsonTransformer** (`json_transformer.py`): Data format transformation

**Response Pattern:**
- POST returns `202 Accepted` with generation status
- GET retrieves stored insights from PostgreSQL (JSONB field)
- Supports async processing via async_pool_executor

---

### Doc Insighter AI Engine

**Overview:** Shared AI-powered document analysis engine using LlamaParse for extraction and CrewAI multi-agent orchestration for intelligent KPI extraction.

#### Core Components

| Component | Purpose |
|-----------|---------|
| **ai_agent.py** | CrewAI agent instantiation and orchestration |
| **extraction_pipeline.py** | Document → structured data extraction workflow |
| **insight_agents.py** | Specialized agents for SOW, WSR, Code Quality, Tech Review, Best Practices analysis |
| **document_kpi_prompts.py** | Prompt templates per document type (6+ agent prompts) |
| **llama_parsing.py** | LlamaParse API integration for document extraction |
| **json_to_markdown.py** | Structured JSON → human-readable markdown conversion |

#### AI Tools

| Tool | Purpose |
|------|---------|
| **AppLogger** | Loguru-based structured logging |
| **FileReaderTool** | CrewAI file reading capability |
| **LlamaTool** | LlamaIndex vector store querying |
| **LLMModels** | Azure OpenAI model config (GPT-4o, embeddings) |
| **StoreDatTool** | Persistent data storage for agent outputs |

#### Supported Document Types

| Document Type | KPI Extraction | Analysis Focus |
|---------------|----------------|-----------------|
| **SOW** | Scope, Deliverables, Timeline, Budget | Project scope & commitments |
| **WSR** | Progress, Metrics, Issues, Risks | Weekly status & health |
| **Code Quality** | Metrics, Violations, Coverage, Standards | Code quality assessment |
| **Tech Review** | Architecture, Design, Standards Compliance | Technical architecture review |
| **Best Practices** | Standards, Patterns, Recommendations | Organizational best practices |

**Processing Flow:**
1. LlamaParse extracts structured content from PDF/DOCX
2. Content routed to specialized agent per document type
3. Agent extracts KPIs using Azure OpenAI GPT-4o
4. Output stored as JSONB in PostgreSQL + raw file in S3

---

### AI Insighter Engine

**Overview:** Additional AI capabilities complementing the Doc Insighter engine.

| Component | Purpose |
|-----------|---------|
| **engine/config.py** | Engine-specific configuration |
| **engine/pipeline.py** | AI processing pipeline |
| **services/project_insighter.py** | Core insight generation logic |
| **services/prompts.py** | Additional prompt templates |

---

## API Endpoints Reference

### Health Check (1 endpoint)

**Application Health & Database Connectivity**
```
GET    /api/v1/health
```

**Description:** Monitor application health and database connectivity  
**Response Codes:** 
- `200`: Application is healthy and database is accessible
- `503`: Application is unhealthy or database is inaccessible

**Example Request:**
```bash
curl -X GET http://localhost:8000/api/v1/health
```

**Example Healthy Response (200):**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-05-07T14:30:00Z",
  "message": "Database connectivity OK (latency: 2ms)"
}
```

**Example Unhealthy Response (503):**
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "timestamp": "2026-05-07T14:30:05Z",
  "message": "Failed to connect to database: connection timeout (5s)"
}
```

**Use Cases:**
- AWS ALB/NLB health checks
- Kubernetes liveness/readiness probes
- Monitoring and alerting systems
- Application startup validation

---

### Complete Endpoint Listing (100+ Total)

#### Finance Module (45+ endpoints)

**Accounts (6 endpoints)**
```
GET    /api/v1/accounts/
POST   /api/v1/accounts/
GET    /api/v1/accounts/{account_id}
PUT    /api/v1/accounts/{account_id}
DELETE /api/v1/accounts/{account_id}
POST   /api/v1/accounts/refresh-account-metrics
```

**Projects (6 endpoints)**
```
GET    /api/v1/projects/
POST   /api/v1/projects/
GET    /api/v1/projects/account/{account_id}
GET    /api/v1/projects/{project_id}
PUT    /api/v1/projects/{project_id}
DELETE /api/v1/projects/{project_id}
```

**Delivery Units (1 endpoint)**
```
GET    /api/v1/delivery_units/
```

**Private Equity (5 endpoints)**
```
POST   /api/v1/finance/private-equity/
GET    /api/v1/finance/private-equity/
GET    /api/v1/finance/private-equity/{pe_id}
PUT    /api/v1/finance/private-equity/{pe_id}
DELETE /api/v1/finance/private-equity/{pe_id}
```

**Dashboard (3 endpoints)**
```
POST   /api/v1/dashboard/
GET    /api/v1/dashboard/get_data
GET    /api/v1/dashboard/account_summary
```

**Data Import/Export (4 endpoints)**
```
POST   /api/v1/import/project
POST   /api/v1/import/revenue
GET    /api/v1/export/all_projects
GET    /api/v1/export/all_revenues
```

**PMO Documents (2 endpoints)**
```
GET    /api/v1/pmo/pmo-files
GET    /api/v1/pmo/revenue-files
```

**Finance Document Processor (20 endpoints)**
```
// SOW Documents
POST   /api/v1/finance/document/import_sow/{project_id}
GET    /api/v1/finance/sow/{project_id}
DELETE /api/v1/finance/sow/{project_id}

// WSR Documents
POST   /api/v1/finance/document/import_wsr/{project_id}
GET    /api/v1/finance/wsr/{project_id}
DELETE /api/v1/finance/wsr/{project_id}

// Code Quality Documents
POST   /api/v1/finance/document/import_code_quality/{project_id}
GET    /api/v1/finance/code_quality/{project_id}
DELETE /api/v1/finance/code_quality/{project_id}

// Tech Review Documents
POST   /api/v1/finance/document/import_tech_review/{project_id}
GET    /api/v1/finance/tech_review/{project_id}
DELETE /api/v1/finance/tech_review/{project_id}

// Best Practices Documents
POST   /api/v1/finance/document/import_best_practices/{project_id}
GET    /api/v1/finance/best_practices/{project_id}
DELETE /api/v1/finance/best_practices/{project_id}

// Project Document Management
GET    /api/v1/finance/document/list/{project_id}/{category}
GET    /api/v1/finance/document/download/{project_id}/{filename}
DELETE /api/v1/finance/document/delete/{project_id}/{filename}

// Private Equity Documents
POST   /api/v1/finance/import/{pe_id}/{document_type}
GET    /api/v1/finance/{pe_id}/{document_type}
DELETE /api/v1/finance/{pe_id}/{document_type}
```

#### Sales Module (35+ endpoints)

**Account Dashboard (5 endpoints)**
```
POST   /api/v1/account-dashboard/
GET    /api/v1/account-dashboard/
GET    /api/v1/account-dashboard/{account_id}
PUT    /api/v1/account-dashboard/{account_id}
DELETE /api/v1/account-dashboard/{account_id}
```

**Stakeholder Details (7 endpoints)**
```
POST   /api/v1/stakeholder-details/
GET    /api/v1/stakeholder-details/
GET    /api/v1/stakeholder-details/{stakeholder_id}
GET    /api/v1/stakeholder-details/account/{account_id}
PUT    /api/v1/stakeholder-details/{stakeholder_id}
DELETE /api/v1/stakeholder-details/{stakeholder_id}
GET    /api/v1/stakeholder-details/search/incumbency/{strength}
```

**Calendar Tasks (3 endpoints)**
```
POST   /api/v1/calendar/tasks/
PUT    /api/v1/calendar/tasks/{task_id}
DELETE /api/v1/calendar/tasks/{task_id}
```

**Calendar Milestones (3 endpoints)**
```
POST   /api/v1/calendar/milestones/
PUT    /api/v1/calendar/milestones/{milestone_id}
DELETE /api/v1/calendar/milestones/{milestone_id}
```

**Calendar Reminders (3 endpoints)**
```
POST   /api/v1/calendar/reminders/
PUT    /api/v1/calendar/reminders/{reminder_id}
DELETE /api/v1/calendar/reminders/{reminder_id}
```

**Calendar Events (1 endpoint)**
```
GET    /api/v1/calendar/events/
```

**Sales Document Processor (20 endpoints - similar structure to Finance)**
```
// SOW, WSR, Code Quality, Tech Review, Best Practices
POST   /api/v1/document/import_{type}/{account_id}
GET    /api/v1/{type}/{account_id}
DELETE /api/v1/{type}/{account_id}

// File Management
GET    /api/v1/document/list/{project_id}/{category}
GET    /api/v1/document/download/{project_id}/{filename}
DELETE /api/v1/document/delete/{project_id}/{filename}
```

**Sales Insights (1 endpoint)**
```
POST   /api/v1/insights/circle-allocation/{project_id}
```

**Sales Export (2 endpoints)**
```
GET    /api/v1/export/accounts
GET    /api/v1/export/stakeholders
```

#### Insights Workflow Module (6 endpoints)

**Project Insights**
```
POST   /api/v1/insights/project/{project_id}
GET    /api/v1/insights/project/{project_id}
```

**Account Insights**
```
POST   /api/v1/insights/account/{account_id}
GET    /api/v1/insights/account/{account_id}
```

**Private Equity Insights**
```
POST   /api/v1/insights/pe/{pe_id}
GET    /api/v1/insights/pe/{pe_id}
```

---

## Database Schema

### Finance Models

```sql
-- Accounts
CREATE TABLE accounts (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  code VARCHAR(50) UNIQUE,
  account_status VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Projects
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES accounts(id),
  project_name VARCHAR(255) NOT NULL,
  start_date DATE,
  end_date DATE,
  budget NUMERIC,
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Delivery Units
CREATE TABLE delivery_units (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  manager_id INTEGER
);

-- Private Equity
CREATE TABLE private_equity (
  id SERIAL PRIMARY KEY,
  pe_name VARCHAR(255) NOT NULL,
  status VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Private Equity Documents
CREATE TABLE private_equity_documents (
  id SERIAL PRIMARY KEY,
  pe_id INTEGER NOT NULL REFERENCES private_equity(id),
  document_type VARCHAR(100),
  s3_key VARCHAR(500),
  metadata JSONB,
  uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Documents (Finance)
CREATE TABLE documents (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id),
  doc_type VARCHAR(100),
  s3_key VARCHAR(500),
  extracted_insights JSONB,
  uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Revenue
CREATE TABLE revenue (
  id SERIAL PRIMARY KEY,
  project_id INTEGER NOT NULL REFERENCES projects(id),
  amount NUMERIC,
  date DATE,
  category VARCHAR(100)
);
```

### Sales Models

```sql
-- Account Dashboards
CREATE TABLE account_dashboards (
  id SERIAL PRIMARY KEY,
  account_id INTEGER,
  pipeline_value NUMERIC,
  win_probability NUMERIC,
  last_updated TIMESTAMP DEFAULT NOW()
);

-- Stakeholder Details
CREATE TABLE stakeholder_details (
  id SERIAL PRIMARY KEY,
  account_id INTEGER,
  name VARCHAR(255),
  email VARCHAR(255),
  role VARCHAR(100),
  incumbency_strength VARCHAR(50)
);

-- Calendar Tasks
CREATE TABLE calendar_tasks (
  id SERIAL PRIMARY KEY,
  project_id INTEGER,
  title VARCHAR(255),
  description TEXT,
  due_date DATE,
  status VARCHAR(50),
  priority VARCHAR(50)
);

-- Calendar Milestones
CREATE TABLE calendar_milestones (
  id SERIAL PRIMARY KEY,
  project_id INTEGER,
  name VARCHAR(255),
  target_date DATE,
  status VARCHAR(50)
);

-- Calendar Reminders
CREATE TABLE calendar_reminders (
  id SERIAL PRIMARY KEY,
  milestone_id INTEGER REFERENCES calendar_milestones(id),
  reminder_date TIMESTAMP,
  message TEXT
);

-- Calendar Reminder Users (Many-to-many)
CREATE TABLE calendar_reminder_users (
  id SERIAL PRIMARY KEY,
  reminder_id INTEGER REFERENCES calendar_reminders(id),
  user_id INTEGER
);
```

### Insights Models

```sql
-- Insight Records (Async Storage)
CREATE TABLE insight_records (
  id SERIAL PRIMARY KEY,
  entity_type VARCHAR(50),  -- 'project', 'account', 'pe'
  entity_id INTEGER,
  insights_json JSONB,
  generated_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## Service Layer Architecture

**20+ Service Classes** organized by module and responsibility:

| Module | Service | Responsibilities |
|--------|---------|------------------|
| **Finance** | AccountService | Account CRUD, metric refresh |
| | ProjectService | Project CRUD, KPI calculation |
| | DeliveryUnitService | Delivery unit retrieval |
| | PrivateEquityService | PE CRUD |
| | RevenueService | Revenue import/export, aggregation |
| | DashboardService | Dashboard data generation |
| | ImportService | Bulk project & revenue import |
| | ExportService | Data export (Excel/CSV) |
| | FileScanner | S3 file validation & scanning |
| | ProjectFileService | S3 file lifecycle (upload/download/delete) |
| **Sales** | AccountDashboardService | Dashboard CRUD |
| | StakeholderDetailsService | Stakeholder CRUD, search |
| | CalendarTaskService | Task CRUD |
| | CalendarMilestoneService | Milestone CRUD |
| | CalendarReminderService | Reminder CRUD |
| | CalendarEventService | Calendar event aggregation |
| | ExportService | Sales data export |
| | ProjectFileService | S3 file lifecycle |
| **Insights** | FinanceInsightsService | Insight generation logic |
| | FinanceAggregationService | Multi-document aggregation |
| | JsonTransformer | Data transformation |
| **Doc Insighter** | CrewAI Agents | Multi-agent orchestration |

---

## Document Processing Pipeline

### 6-Stage Processing Workflow

```
┌──────────────────────────────────────────────────────────────┐
│                 DOCUMENT PROCESSING PIPELINE                  │
└──────────────────────────────────────────────────────────────┘

STAGE 1: UPLOAD & VALIDATION
├─ Receive file via FastAPI endpoint (multipart/form-data)
├─ Validate file type (.pdf, .docx, .doc, .txt, .pptx, .xlsx, .csv)
├─ Validate file size (max configurable)
├─ Check permissions (account_id/project_id ownership)
└─ Generate unique filename: {uuid8}_{FILETYPE}_{original}_{timestamp}{ext}

STAGE 2: S3 STORAGE & METADATA
├─ Upload to S3 with structured path
│  └─ Finance: s3://{bucket}/uploaded_docs/pmo/{project_id}/
│  └─ Sales: s3://{bucket}/uploaded_docs/project_docs/{account_id}/
├─ Store metadata in PostgreSQL (Document model)
├─ Record: doc_type, s3_key, uploaded_at, project_id/account_id
└─ On failure: Move to pmo_failed/ or project_docs_failed/

STAGE 3: DOCUMENT EXTRACTION (LlamaParse)
├─ Call LlamaCloud API with S3 file
├─ Extract structured content:
│  ├─ Text sections & paragraphs
│  ├─ Tables (structured as JSON)
│  ├─ Images & diagrams
│  └─ Metadata (title, author, creation date)
└─ Return parsed JSON to backend

STAGE 4: AI ANALYSIS (CrewAI + Azure OpenAI)
├─ Route to document-type-specific agent
├─ Agent uses document_kpi_prompts.py template
├─ Extract structured KPIs:
│  ├─ SOW: scope, deliverables, timeline, budget
│  ├─ WSR: progress, metrics, issues, risks
│  ├─ Code Quality: metrics, violations, coverage
│  ├─ Tech Review: architecture, design, standards
│  └─ Best Practices: standards, patterns, recommendations
├─ Use Azure OpenAI GPT-4o for extraction
└─ Output: Structured JSON KPI object

STAGE 5: DATABASE PERSISTENCE
├─ Store extracted_insights (JSONB) in Document model
├─ Update Document record with:
│  ├─ extracted_insights: {kpis, summary, metrics}
│  ├─ processing_status: 'success' | 'partial' | 'failed'
│  └─ processed_at: timestamp
├─ Create relationship: Project/Account → Document
└─ Trigger insight regeneration for Insights Workflow

STAGE 6: RETRIEVAL & DELIVERY
├─ GET endpoint returns:
│  ├─ Document metadata (uploaded_at, doc_type, s3_key)
│  ├─ Extracted KPIs from JSONB field
│  ├─ S3 presigned URL (1-hour expiry)
│  └─ Processing status
├─ Generate S3 presigned URL for download
└─ Support deletion (remove Document record + S3 file)

┌──────────────────────────────────────────────────────────────┐
│ Tools Used Throughout Pipeline                                │
├──────────────────────────────────────────────────────────────┤
│ • doc_importer.py — Upload validation & S3 upload             │
│ • s3_storage.py — S3 client wrapper (upload/download/delete)  │
│ • llama_parsing.py — LlamaParse API integration               │
│ • ai_agent.py — CrewAI agent instantiation                    │
│ • document_kpi_prompts.py — Agent prompt templates            │
│ • app_logger.py — Structured logging (Loguru)                 │
│ • async_pool_executor.py — Async processing for long uploads  │
└──────────────────────────────────────────────────────────────┘
```

### Example Processing Flow

```
1. User uploads SOW.pdf via /api/v1/finance/document/import_sow/{project_id}

2. Backend validates:
   ├─ File size < 50MB ✓
   ├─ File type = .pdf ✓
   ├─ Project exists & accessible ✓
   └─ Generate: 9c8d7e6f_SOW_proposal_20260507_143022.pdf

3. Upload to S3:
   └─ s3://{bucket}/uploaded_docs/pmo/{project_id}/9c8d7e6f_SOW_proposal_20260507_143022.pdf

4. Store metadata in Document:
   ├─ project_id = 123
   ├─ doc_type = 'SOW'
   ├─ s3_key = 'uploaded_docs/pmo/123/9c8d7e6f_SOW_proposal_20260507_143022.pdf'
   └─ uploaded_at = 2026-05-07 14:30:22

5. Extract via LlamaParse:
   └─ Structured JSON: {sections: [...], tables: [...], metadata: {...}}

6. CrewAI SOW Agent analyzes:
   ├─ Extracts scope: "Cloud infrastructure migration for retail platform"
   ├─ Extracts deliverables: ["Design doc", "Implementation", "UAT"]
   ├─ Extracts timeline: "6 months (Jun-Nov 2026)"
   ├─ Extracts budget: "$500,000"
   └─ Output: {scope: "...", deliverables: [...], timeline: "...", budget: "$500,000"}

7. Store in PostgreSQL:
   └─ Document.extracted_insights = {
       "scope": "Cloud infrastructure migration...",
       "deliverables": ["Design doc", ...],
       "timeline": "6 months (Jun-Nov 2026)",
       "budget": "$500,000"
     }

8. GET /api/v1/finance/sow/123 returns:
   ├─ Document metadata
   ├─ Extracted KPIs from JSONB
   ├─ S3 presigned URL
   └─ Success status

9. Trigger Insights Workflow:
   └─ POST /api/v1/insights/project/123 → 202 Accepted
      └─ Aggregates all project documents (SOW, WSR, Code Quality, etc.)
         → Generates comprehensive project insights
```

---

## Insight Generation Flow

### Async Multi-Agent Insight Pattern

```
┌──────────────────────────────────────────────────────────────┐
│              ASYNC INSIGHT GENERATION FLOW                    │
└──────────────────────────────────────────────────────────────┘

REQUEST:
├─ POST /api/v1/insights/project/{project_id}
├─ Returns: 202 Accepted
│  └─ Response: {"status": "generating", "entity_id": 123, "entity_type": "project"}
└─ Backend enqueues async job (async_pool_executor)

BACKEND PROCESSING (Async):
├─ STEP 1: Retrieve all documents for project
│  └─ Query: Documents.filter(project_id=123) with extracted_insights populated
│
├─ STEP 2: Initialize GeneralizedCrew (Multi-Agent Orchestration)
│  ├─ Create agents per analysis type:
│  │  ├─ SOW Analyzer Agent
│  │  ├─ WSR Analyst Agent
│  │  ├─ Code Quality Auditor Agent
│  │  ├─ Tech Architecture Reviewer Agent
│  │  └─ Best Practices Assessor Agent
│  │
│  └─ Load ContextAwareAgents configuration for "project" entity
│
├─ STEP 3: Multi-Agent Analysis
│  ├─ Agent 1: Analyze SOW document
│  │  └─ Extract: scope, deliverables, timeline, budget
│  ├─ Agent 2: Analyze WSR documents (latest 10)
│  │  └─ Extract: progress %, key metrics, issues, risks
│  ├─ Agent 3: Code Quality analysis
│  │  └─ Extract: quality score, violations, coverage %
│  ├─ Agent 4: Tech review analysis
│  │  └─ Extract: architecture fit, standards compliance, tech debt
│  └─ Agent 5: Best practices review
│     └─ Extract: process compliance, recommendations
│
├─ STEP 4: Aggregation (FinanceAggregationService)
│  ├─ Cross-document analysis:
│  │  ├─ Timeline accuracy (SOW vs WSR progress)
│  │  ├─ Budget health (SOW budget vs actual spend)
│  │  ├─ Quality trajectory (Code Quality trends)
│  │  ├─ Risk assessment (WSR risks + Tech Review concerns)
│  │  └─ Recommendations synthesis
│  │
│  └─ Generate comprehensive project insight:
│     └─ {
│          "project_id": 123,
│          "project_name": "...",
│          "overall_health": "green|amber|red",
│          "timeline_status": "on_track|at_risk|delayed",
│          "budget_status": "within_budget|overage",
│          "quality_metrics": {...},
│          "risks": [...],
│          "recommendations": [...],
│          "generated_at": "2026-05-07T14:35:00Z"
│        }
│
├─ STEP 5: Persistence (PostgreSQL)
│  └─ InsightRecord:
│     ├─ entity_type: "project"
│     ├─ entity_id: 123
│     ├─ insights_json: {...comprehensive insight...}
│     ├─ generated_at: timestamp
│     └─ updated_at: timestamp
│
└─ STEP 6: Mark as complete
   └─ Send completion notification (if webhook configured)

RETRIEVAL:
├─ GET /api/v1/insights/project/{project_id}
├─ Query: InsightRecord.filter(entity_type='project', entity_id=123)
└─ Return: Stored insights_json with full analysis

STATUS CODES:
├─ 202 Accepted — Insight generation queued
├─ 200 OK — Insight successfully retrieved
├─ 404 Not Found — No insights generated yet (call POST to generate)
└─ 500 Server Error — Generation failed (check logs)
```

### Architecture Components

| Component | Role |
|-----------|------|
| **GeneralizedCrew** | Multi-agent orchestration engine; manages all agents, tool allocation, communication |
| **ContextAwareAgents** | Dynamic configuration; adapts agents for project/account/PE contexts |
| **FinanceInsightsService** | Coordinates multi-agent analysis, prompts agents in sequence |
| **FinanceAggregationService** | Cross-document synthesis, produces final insight JSON |
| **JsonTransformer** | Converts raw agent outputs to standardized insight schema |
| **async_pool_executor** | ThreadPoolExecutor for async processing without blocking API |

---

## S3 Storage Layout

### Folder Structure

```
s3://{S3_BUCKET_NAME}/uploaded_docs/

├── pmo/                             # Finance document uploads
│   ├── {project_id}/
│   │   ├── {uuid8}_SOW_{name}_{timestamp}.pdf
│   │   ├── {uuid8}_WSR_{name}_{timestamp}.docx
│   │   ├── {uuid8}_CODE_QUALITY_{name}_{timestamp}.pdf
│   │   ├── {uuid8}_TECH_REVIEW_{name}_{timestamp}.pdf
│   │   └── {uuid8}_BEST_PRACTICES_{name}_{timestamp}.docx
│   └── ...
│
├── pmo_failed/                      # Finance failed uploads (for auditing)
│   ├── {project_id}/
│   └── ...
│
├── project_docs/                    # Sales document uploads
│   ├── {account_id}/
│   │   ├── {uuid8}_SOW_{name}_{timestamp}.pdf
│   │   ├── {uuid8}_WSR_{name}_{timestamp}.docx
│   │   ├── {uuid8}_CODE_QUALITY_{name}_{timestamp}.pdf
│   │   ├── {uuid8}_TECH_REVIEW_{name}_{timestamp}.pdf
│   │   └── {uuid8}_BEST_PRACTICES_{name}_{timestamp}.docx
│   └── ...
│
└── project_docs_failed/             # Sales failed uploads
    ├── {account_id}/
    └── ...
```

### Filename Format

**Pattern:** `{uuid8}_{FILETYPE}_{original_name}_{timestamp}{extension}`

**Example:** `9c8d7e6f_SOW_proposal_draft_20260507_143022.pdf`

- **uuid8** — First 8 characters of UUID4 (unique identifier)
- **FILETYPE** — One of: SOW, WSR, CODE_QUALITY, TECH_REVIEW, BEST_PRACTICES
- **original_name** — Original filename stem, sanitized (spaces→underscores)
- **timestamp** — YYYYMMDD_HHMMSS (local to upload server)
- **extension** — Original file extension (.pdf, .docx, .doc, .txt, .pptx, .xlsx, .csv)

### Presigned URL Generation

Download endpoints (`/api/v1/*/document/download/{project_id}/{filename}`) return:
- S3 presigned URL (1-hour expiry)
- File metadata (size, upload date, doc type)
- Content-Disposition headers for proper file download

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

### Database Configuration

```env
# PostgreSQL (Supabase)
user=postgres
password=<your_secure_password>
host=db.your-project.supabase.co
port=5432
dbname=postgres
SYSTEM_USER_ID=550e8400-e29b-41d4-a716-446655440000
```

### AWS S3 Configuration

```env
# AWS S3 for document uploads
S3_BUCKET_NAME=nit-project-insighter
AWS_ACCESS_KEY_ID=<your_access_key>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
AWS_DEFAULT_REGION=ap-southeast-2
```

### Azure OpenAI Configuration

```env
# Azure OpenAI (GPT-4o for document analysis)
AZURE_API_KEY=<your_azure_openai_key>
AZURE_API_BASE=https://your-resource.openai.azure.com
AZURE_API_VERSION=2024-02-15-preview
AZURE_DEPLOYMENT_NAME=gpt-4o
```

### LlamaParse Configuration

```env
# LlamaParse API for document extraction
LLAMA_CLOUD_API_KEY=<your_llama_cloud_key>
```

### Application Configuration

```env
# App-specific settings
TEMP_DIR=/tmp
SUPPORTED_DOC_TYPE_EXTENSIONS=.pdf,.docx,.doc,.txt,.pptx,.xlsx,.csv
```

---

## Local Development

### Prerequisites

- **Python 3.12+** (check with `python --version`)
- **uv** package manager ([install](https://docs.astral.sh/uv/))
- **PostgreSQL database** (local or Supabase)
- **AWS credentials** configured (for S3 access)

### Setup Steps

1. **Clone the repository**

```bash
git clone https://github.com/your-org/project-insighter-backend.git
cd project-insighter-backend
```

2. **Install dependencies**

```bash
uv sync
```

This installs all dependencies listed in `pyproject.toml` into a virtual environment.

3. **Create `.env` file**

```bash
# Copy the environment template
cp .env.example .env

# Edit with your credentials
nano .env
```

Required variables (see [Environment Variables](#environment-variables) section above):
- Database: `user`, `password`, `host`, `port`, `dbname`, `SYSTEM_USER_ID`
- AWS S3: `S3_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
- Azure OpenAI: `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION`, `AZURE_DEPLOYMENT_NAME`
- LlamaParse: `LLAMA_CLOUD_API_KEY`
- App: `TEMP_DIR`, `SUPPORTED_DOC_TYPE_EXTENSIONS`

4. **Run the application**

```bash
uv run python main.py
```

The API will be available at `http://localhost:8000` with interactive Swagger UI at `http://localhost:8000/docs`.

### Docker Compose (Local)

For a fully containerized local environment:

```bash
docker-compose up --build
```

This spins up the FastAPI application in a container with all dependencies.

### Development Tips

- **Database tables auto-created** — Run `main.py` once to create all tables via `Base.metadata.create_all()`
- **Swagger UI** — Access `http://localhost:8000/docs` for interactive API testing
- **Hot reload** — Uvicorn automatically reloads on code changes when running via `uv run`
- **Logs** — Check terminal output for request logs and errors (Loguru)
- **S3 Testing** — Ensure AWS credentials are configured for S3 upload testing

---

## Docker Deployment

### AWS Lambda Deployment Pipeline

The application is containerized and deployed to **AWS Lambda** via **Amazon ECR** (Elastic Container Registry).

#### Architecture

- **Dockerfile** — Builds Docker image using AWS Lambda Python 3.12 base image
- **main.py** — Exports `handler = Mangum(app)` for Lambda ASGI compatibility
- **ECR** — Stores Docker images tagged by version/environment
- **Lambda Function** — Pulls image from ECR and executes on API Gateway events

#### Deployment Steps

**1. Authenticate with ECR**

```bash
aws ecr get-login-password --region ap-southeast-2 | \
  docker login --username AWS --password-stdin \
  {AWS_ACCOUNT_ID}.dkr.ecr.ap-southeast-2.amazonaws.com
```

Replace `{AWS_ACCOUNT_ID}` with your AWS account ID.

**2. Build Docker image (Linux/AMD64 for Lambda)**

```bash
docker build --platform linux/amd64 --provenance=false \
  -t project-insighter-backend .
```

**3. Tag the image for ECR**

```bash
docker tag project-insighter-backend:latest \
  {AWS_ACCOUNT_ID}.dkr.ecr.ap-southeast-2.amazonaws.com/project-insighter-backend:latest
```

**4. Push to ECR**

```bash
docker push {AWS_ACCOUNT_ID}.dkr.ecr.ap-southeast-2.amazonaws.com/project-insighter-backend:latest
```

**5. Update Lambda function**

Go to AWS Lambda Console:
1. Select your function (`project-insighter-backend` or similar)
2. Scroll to "Image" section
3. Click "Deploy new image"
4. Paste ECR image URI: `{AWS_ACCOUNT_ID}.dkr.ecr.ap-southeast-2.amazonaws.com/project-insighter-backend:latest`
5. Click "Deploy"

**6. Configure environment variables in Lambda**

In Lambda Console → Configuration → Environment variables, add:
- `user`, `password`, `host`, `port`, `dbname` (Database)
- `S3_BUCKET_NAME`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION` (S3)
- `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION`, `AZURE_DEPLOYMENT_NAME` (Azure OpenAI)
- `LLAMA_CLOUD_API_KEY` (LlamaParse)
- `TEMP_DIR=/tmp`, `SUPPORTED_DOC_TYPE_EXTENSIONS` (App)

**7. Verify deployment**

Test the Lambda function via API Gateway:
```bash
curl https://your-api-gateway-url/api/v1/accounts
```

#### Dockerfile Overview

```dockerfile
FROM public.ecr.aws/lambda/python:3.12

COPY pyproject.toml ${LAMBDA_TASK_ROOT}/
COPY . ${LAMBDA_TASK_ROOT}/

RUN pip install uv && uv sync

CMD [ "main.handler" ]
```

- Uses AWS Lambda Python 3.12 base image
- Installs `uv` and dependencies from `pyproject.toml`
- Exports `handler` from `main.py` (Mangum ASGI adapter)

#### Important Notes

- **Memory & Timeout** — Configure Lambda function memory (1GB+ recommended) and timeout (300s+ for document processing)
- **IAM Roles** — Lambda execution role needs permissions for:
  - S3 bucket read/write (`s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`)
  - Supabase PostgreSQL network connectivity (VPC/security group)
  - CloudWatch Logs (auto-configured)
- **Cold Start** — First request takes ~5-10s (Python startup + dependency loading); subsequent requests are faster
- **Concurrency** — Set reserved concurrency if needed to control costs/scaling

---

## License

Private — Internal use only.

---

**Last Updated:** May 7, 2026  
**Version:** 2.0 (Comprehensive Rewrite)  
**Author:** GitHub Copilot
