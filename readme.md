# Project Insighter Backend

A FastAPI backend powering project management, financial tracking, sales pipeline, and AI-driven document analysis. Deployed on **AWS Lambda** via Docker container images pushed to **ECR**.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Modules](#modules)
- [API Endpoints](#api-endpoints)
- [S3 Storage Layout](#s3-storage-layout)
- [Environment Variables](#environment-variables)
- [Local Development](#local-development)
- [Docker Deployment (AWS)](#docker-deployment-aws)
- [Database](#database)

---

## Architecture Overview

```
                    ┌──────────────┐
                    │  CloudFront  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  API Gateway │
                    └──────┬───────┘
                           │
                ┌──────────▼──────────┐
                │   AWS Lambda        │
                │   (Docker/Mangum)   │
                └──┬──────┬───────┬──┘
                   │      │       │
            ┌──────▼┐ ┌───▼───┐ ┌─▼──────┐
            │Postgres│ │  S3   │ │Azure AI│
            │(Supa)  │ │Bucket │ │(GPT-4o)│
            └────────┘ └───────┘ └────────┘
```

---

## Project Structure

```
project-insighter-backend/
├── main.py                          # FastAPI app + Mangum Lambda handler
├── pyproject.toml                   # Dependencies (uv/pip)
├── Dockerfile                       # AWS Lambda Python 3.12 image
├── docker-compose.yml               # Local Docker setup
├── backend/
│   ├── core/
│   │   └── config.py                # Unified settings (BaseAppSettings)
│   ├── db/
│   │   ├── base.py                  # SQLAlchemy declarative Base
│   │   └── session.py               # DB engine, SessionLocal, get_db()
│   ├── doc_insighter/
│   │   ├── core/                    # AI agent pipeline
│   │   │   ├── ai_agent.py          # CrewAI agent orchestration
│   │   │   ├── extraction_pipeline.py
│   │   │   ├── document_kpi_prompts.py
│   │   │   ├── insight_agents.py    # Multi-agent SOW/WSR analysis
│   │   │   ├── json_to_markdown.py
│   │   │   └── llama_parsing.py     # LlamaParse document extraction
│   │   └── tools/
│   │       ├── app_logger.py        # Loguru-based logger
│   │       ├── file_reader_tool.py  # CrewAI file reader tool
│   │       ├── llama_tool.py        # LlamaIndex query tool
│   │       ├── llm_models.py        # Azure OpenAI model config
│   │       └── store_data.py        # Data persistence tool
│   ├── finance/
│   │   ├── app/
│   │   │   ├── api/                 # Account, Project, DU, Dashboard, Import/Export, PMO
│   │   │   ├── models/              # SQLAlchemy models
│   │   │   ├── schemas/             # Pydantic schemas
│   │   │   └── services/            # Business logic
│   │   └── doc_processor/
│   │       ├── api/                 # SOW, WSR, Code Quality, Tech Review, Best Practices, Project Docs
│   │       └── services/            # Document processing + S3 file service
│   ├── sales/
│   │   ├── app/
│   │   │   ├── api/                 # Account Dashboard, Calendar (Tasks/Milestones/Reminders/Events), Stakeholders, Export
│   │   │   ├── models/
│   │   │   ├── schemas/
│   │   │   └── services/
│   │   └── doc_processor/
│   │       ├── api/                 # SOW, WSR, Code Quality, Tech Review, Best Practices, Project Docs, Insights
│   │       └── services/            # Document processing + S3 file service + Insight service
│   └── utitlites/
│       ├── app_utilites.py          # safe_float, safe_int helpers
│       ├── async_pool_executor.py   # ThreadPoolExecutor for sync-in-async
│       ├── doc_importer.py          # File upload → S3 → AI processing pipeline
│       └── s3_storage.py            # S3 upload/download/list/delete/presigned URLs
```

---

## Tech Stack

| Layer           | Technology                                                    |
|-----------------|---------------------------------------------------------------|
| **Framework**   | FastAPI + Uvicorn                                             |
| **Runtime**     | Python 3.12                                                   |
| **ORM**         | SQLAlchemy 2.x (sync)                                         |
| **Database**    | PostgreSQL (Supabase)                                         |
| **Validation**  | Pydantic v2 + pydantic-settings                               |
| **AI/LLM**      | Azure OpenAI (GPT-4o), CrewAI, LlamaIndex, LlamaParse        |
| **Storage**     | AWS S3 (boto3)                                                |
| **Deployment**  | AWS Lambda (Docker) + API Gateway + ECR                       |
| **Adapter**     | Mangum (ASGI → Lambda)                                        |
| **Pkg Manager** | uv                                                            |

---

## Modules

### Finance (`/api/v1/...` and `/api/v1/finance/...`)

| Area              | Description                                                  |
|-------------------|--------------------------------------------------------------|
| **Accounts**      | CRUD for client accounts                                     |
| **Projects**      | CRUD for projects under accounts                             |
| **Delivery Units**| CRUD for organizational delivery units                       |
| **Dashboard**     | Aggregated financial KPIs and metrics                        |
| **Import/Export** | Bulk Excel/CSV data import and export                        |
| **PMO Docs**      | AI-powered document analysis (SOW, WSR, Code Quality, etc.) |

### Sales (`/api/v1/...`)

| Area              | Description                                                  |
|-------------------|--------------------------------------------------------------|
| **Account Dashboard** | Sales account overview and metrics                       |
| **Stakeholders**  | Contact and stakeholder management                           |
| **Calendar**      | Tasks, Milestones, Reminders, Events for project planning    |
| **Doc Processor** | AI document analysis (same doc types as Finance)             |
| **Insights**      | AI-driven team/circle allocation from SOW+WSR analysis       |

### Doc Insighter (Shared AI Engine)

- **LlamaParse** for document extraction (PDF, DOCX, PPTX, TXT)
- **CrewAI agents** with Azure OpenAI GPT-4o for structured KPI extraction
- **Prompt templates** for SOW, WSR, Code Quality, Best Practices, Tech Review
- **Multi-agent insight pipeline** for cross-document analysis

---

## API Endpoints

### Sales

| Method | Path                                              | Description                      |
|--------|---------------------------------------------------|----------------------------------|
| GET    | `/api/v1/account-dashboard/`                      | List account dashboards          |
| POST   | `/api/v1/account-dashboard/`                      | Create account dashboard         |
| GET    | `/api/v1/stakeholder-details/`                    | List stakeholders                |
| POST   | `/api/v1/stakeholder-details/`                    | Create stakeholder               |
| CRUD   | `/api/v1/calendar/tasks/`                         | Calendar tasks                   |
| CRUD   | `/api/v1/calendar/milestones/`                    | Calendar milestones              |
| CRUD   | `/api/v1/calendar/reminders/`                     | Calendar reminders               |
| GET    | `/api/v1/calendar/events/`                        | Calendar events view             |
| POST   | `/api/v1/document/import_sow/{account_id}`        | Upload SOW document              |
| POST   | `/api/v1/document/import_wsr/{account_id}`        | Upload WSR document              |
| POST   | `/api/v1/document/import_code_quality/{account_id}`| Upload Code Quality doc         |
| POST   | `/api/v1/document/import_tech_review/{account_id}`| Upload Tech Review doc           |
| POST   | `/api/v1/document/import_best_practices/{account_id}`| Upload Best Practices doc     |
| GET    | `/api/v1/document/list/{project_id}/{category}`   | List uploaded files by category  |
| GET    | `/api/v1/document/download/{project_id}/{filename}`| Download file (S3 presigned)    |
| POST   | `/api/v1/insights/circle-allocation/{project_id}` | AI circle/team allocation        |

### Finance

| Method | Path                                                  | Description                    |
|--------|-------------------------------------------------------|--------------------------------|
| CRUD   | `/api/v1/accounts/`                                   | Finance accounts               |
| CRUD   | `/api/v1/projects/`                                   | Finance projects               |
| CRUD   | `/api/v1/delivery-units/`                             | Delivery units                 |
| GET    | `/api/v1/dashboard/`                                  | Finance dashboard data         |
| POST   | `/api/v1/import/`                                     | Bulk data import               |
| GET    | `/api/v1/export/`                                     | Data export                    |
| GET    | `/api/v1/pmo/`                                        | PMO document endpoints         |
| POST   | `/api/v1/finance/document/import_sow/{project_id}`   | Upload SOW (finance)           |
| POST   | `/api/v1/finance/document/import_wsr/{project_id}`   | Upload WSR (finance)           |
| POST   | `/api/v1/finance/document/import_code_quality/{project_id}` | Upload Code Quality     |
| POST   | `/api/v1/finance/document/import_tech_review/{project_id}`  | Upload Tech Review      |
| POST   | `/api/v1/finance/document/import_best_practices/{project_id}`| Upload Best Practices  |
| GET    | `/api/v1/finance/document/list/{project_id}/{category}`     | List files by category  |
| GET    | `/api/v1/finance/document/download/{project_id}/{filename}` | Download (S3 presigned) |

---

## S3 Storage Layout

All uploaded documents are stored in S3 with this structure:

```
s3://{S3_BUCKET_NAME}/uploaded_docs/
├── pmo/{project_id}/                    ← Finance doc processor
│   ├── a1b2c3d4_SOW_proposal_20260404_120000.pdf
│   ├── e5f6a7b8_WSR_weekly-report_20260404_130000.docx
│   └── ...
├── pmo_failed/{project_id}/             ← Finance failed uploads
├── project_docs/{account_id}/           ← Sales doc processor
│   ├── 9c8d7e6f_CODE_QUALITY_review_20260404_140000.pdf
│   └── ...
└── project_docs_failed/{account_id}/    ← Sales failed uploads
```

**Filename format:** `{uuid8}_{FILETYPE}_{original_name}_{timestamp}{extension}`

- `uuid8` — first 8 chars of a UUID4
- `FILETYPE` — `SOW`, `WSR`, `CODE_QUALITY`, `TECH_REVIEW`, `BEST_PRACTICES`
- `original_name` — original filename stem (without extension)
- `timestamp` — `YYYYMMDD_HHMMSS`
- `extension` — original file extension (`.pdf`, `.docx`, etc.)

---

## Environment Variables

Create a `.env` file in the project root:

```env
# Database (PostgreSQL / Supabase)
user=postgres
password=your_db_password
host=db.your-project.supabase.co
port=5432
dbname=postgres
SYSTEM_USER_ID=550e8400-e29b-41d4-a716-446655440000

# AWS S3
S3_BUCKET_NAME=nit-project-insighter
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=ap-southeast-2

# Azure OpenAI
AZURE_API_KEY=your_azure_key
AZURE_API_BASE=https://your-resource.openai.azure.com
AZURE_API_VERSION=2024-02-15-preview
AZURE_DEPLOYMENT_NAME=gpt-4o

# LlamaParse
LLAMA_CLOUD_API_KEY=your_llama_key

# App Config
TEMP_DIR=/tmp
SUPPORTED_DOC_TYPE_EXTENSIONS=.pdf,.docx,.doc,.txt,.pptx,.xlsx,.csv
```

---

## Local Development

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- PostgreSQL database (or Supabase)
- AWS credentials configured

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/project-insighter-backend.git
cd project-insighter-backend

# Install dependencies
uv sync

# Create .env file with required variables (see above)
cp .env.example .env

# Run the server
uv run python main.py
```

The API will be available at `http://localhost:8000` with Swagger docs at `http://localhost:8000/docs`.

### Docker (Local)

```bash
docker-compose up --build
```

---

## Docker Deployment (AWS)

The application is deployed as a Docker container on **AWS Lambda** via **ECR**.

### 1. Authenticate with ECR

```bash
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 2*************9.dkr.ecr.ap-southeast-2.amazonaws.com
```

### 2. Build the Docker image

```bash
docker build --platform linux/amd64 --provenance=false -t project-insighter-backend .
```

### 3. Tag the image

```bash
docker tag project-insighter-backend:latest 2*************9.dkr.ecr.ap-southeast-2.amazonaws.com/project-insighter-backend:latest
```

### 4. Push to ECR

```bash
docker push 2*************9.dkr.ecr.ap-southeast-2.amazonaws.com/project-insighter-backend:latest
```

> After pushing, update the Lambda function to use the new image. Environment variables are configured in the Lambda function settings.

---

## Database

Single **PostgreSQL** database (hosted on Supabase) shared by both Finance and Sales modules.

**Key tables:**

| Module   | Models                                                              |
|----------|---------------------------------------------------------------------|
| Finance  | Account, Project, DeliveryUnit, ProjectDocument, Revenue            |
| Sales    | AccountDashboard, StakeholderDetails, CalendarTask, CalendarMilestone, CalendarReminder, CalendarReminderUsers, AccountDocument |

The database schema is auto-created on startup via `Base.metadata.create_all()`.

---

## License

Private — Internal use only.