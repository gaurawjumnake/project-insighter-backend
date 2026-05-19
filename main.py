from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.sales.app.api import stakeholder_details
from backend.db.base import Base
from backend.db.session import engine
from backend.sales.app import models
from backend.sales.app.api import (
    calendar_task
)
from backend.sales.doc_processor.api import sow as sow_api
from backend.sales.doc_processor.api import wsr as wsr_api
from backend.sales.doc_processor.api import code_quality as code_quality_api
from backend.sales.doc_processor.api import tech_review as tech_review_api
from backend.sales.doc_processor.api import best_practices as best_practices_api
from backend.sales.doc_processor.api import project_docs as project_docs_api
from backend.sales.doc_processor.api import insights as sales_insights_api
from backend.sales.app.api import account_dashboard, calendar_event, calendar_milestone, calendar_reminder

# Finance imports
from backend.finance.app.api import account as fin_account
from backend.finance.app.api import project as fin_project
from backend.finance.app.api import delivery_unit as fin_delivery_unit
from backend.finance.app.api import dashboard as fin_dashboard
from backend.finance.app.api import export_data as fin_export_data
from backend.finance.app.api import import_data as fin_import_data
from backend.finance.app.api import pmo_docs as fin_pmo_docs
from backend.finance.app.api import private_equity as fin_private_equity
# from backend.finance.app.api import health as fin_health

# from backend.insights_workflow.api import insights as fin_insights
from backend.ai_insighter.api import insighter_api as ai_insights
from backend.ai_insighter.api import any_doc_insighter_api as any_docs_api

from backend.finance.doc_processor.api import sow as fin_sow_api
from backend.finance.doc_processor.api import wsr as fin_wsr_api
from backend.finance.doc_processor.api import code_quality as fin_code_quality_api
from backend.finance.doc_processor.api import tech_review as fin_tech_review_api
from backend.finance.doc_processor.api import best_practices as fin_best_practices_api
from backend.finance.doc_processor.api import project_docs as fin_project_docs_api
from backend.finance.doc_processor.api import private_equity_docs as pe_docs_api

# Optional: Create tables automatically on startup (useful for dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Account & Stakeholder API",
    description="API for managing Account Dashboards and Stakeholder Details stored in Supabase",
    version="1.0.0"
)

# CORS Configuration (allows frontend to talk to backend)
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "https://d2qy9zmdaxe9p6.cloudfront.net"
    # Add your frontend URL here if different
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(
    account_dashboard.router,
    prefix="/api/v1/account-dashboard",
    tags=["Account Dashboard"]
)

app.include_router(
    stakeholder_details.router,
    prefix="/api/v1/stakeholder-details",
    tags=["Stakeholder Details"]
)
app.include_router(calendar_task.router, prefix="/api/v1/calendar/tasks", tags=["Calendar Tasks"])
app.include_router(calendar_milestone.router, prefix="/api/v1/calendar/milestones", tags=["Calendar Milestones"])
app.include_router(calendar_reminder.router, prefix="/api/v1/calendar/reminders", tags=["Calendar Reminders"])
app.include_router(calendar_event.router, prefix="/api/v1/calendar/events", tags=["Calendar View"])
app.include_router(sow_api.router,  prefix="/api/v1")
app.include_router(wsr_api.router,  prefix="/api/v1")
app.include_router(code_quality_api.router, prefix="/api/v1")
app.include_router(tech_review_api.router, prefix="/api/v1")
app.include_router(best_practices_api.router, prefix="/api/v1")
app.include_router(project_docs_api.router, prefix="/api/v1")
app.include_router(sales_insights_api.router, prefix="/api/v1")

# Finance App Routers
app.include_router(fin_account.router, prefix="/api/v1", tags=["Finance Accounts"])
app.include_router(fin_project.router, prefix="/api/v1", tags=["Finance Projects"])
app.include_router(fin_delivery_unit.router, prefix="/api/v1", tags=["Finance Delivery Units"])
app.include_router(fin_dashboard.router, prefix="/api/v1", tags=["Finance Dashboard"])
app.include_router(fin_export_data.router, prefix="/api/v1", tags=["Finance Export"])
app.include_router(fin_import_data.router, prefix="/api/v1", tags=["Finance Import"])
app.include_router(fin_pmo_docs.router, prefix="/api/v1/pmo", tags=["Finance PMO Docs"])
app.include_router(fin_private_equity.router, prefix="/api/v1/finance", tags=["Private Equity"])
# app.include_router(fin_health.router, prefix="/api/v1", tags=["Health Check"])

app.include_router(ai_insights.router, tags=["AI Insights"])
app.include_router(any_docs_api.router, tags=["Any Docs"])

# Finance Doc Processor Routers
app.include_router(fin_sow_api.router, prefix="/api/v1/finance")
app.include_router(fin_wsr_api.router, prefix="/api/v1/finance")
app.include_router(fin_code_quality_api.router, prefix="/api/v1/finance")
app.include_router(fin_tech_review_api.router, prefix="/api/v1/finance")
app.include_router(fin_best_practices_api.router, prefix="/api/v1/finance")
app.include_router(fin_project_docs_api.router, prefix="/api/v1/finance")
app.include_router(pe_docs_api.router, prefix="/api/v1/finance")

from mangum import Mangum
handler = Mangum(app=app)

# app.include_router(
#     export_data.router,
#     prefix="/api/v1/export-data",
#     tags=["Export Data"]
# )

@app.get("/")
def read_root():
    return {"status":200,
        "message": "Welcome to the Account & Stakeholder API"}

# If running directly with python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
