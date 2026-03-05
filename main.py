from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import account_dashboard, stakeholder_details
from backend.app.db.base import Base
from backend.app.db.session import engine
from backend.app import models
from backend.app.api import (
    calendar_task, 
    calendar_milestone, 
    calendar_reminder, 
    calendar_event
)
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

from mangum import Mangum
handler = Mangum(app=app)

# app.include_router(
#     export_data.router,
#     prefix="/api/v1/export-data",
#     tags=["Export Data"]
# )
@app.get("/")
def read_root():
    return {"message": "Welcome to the Account & Stakeholder API"}

# If running directly with python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
