# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from backend.app.api import api_router

# # Create FastAPI application
# app = FastAPI(
#     title="Project Insighter API",
#     description="API for managing account dashboards and stakeholder details",
#     version="1.0.0"
# )

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, replace with specific origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include API router
# app.include_router(api_router, prefix="/api/v1")


# @app.get("/")
# def root():
#     """Root endpoint."""
#     return {
#         "message": "Welcome to Project Insighter API",
#         "docs": "/docs",
#         "version": "1.0.0"
#     }


# @app.get("/health")
# def health_check():
#     """Health check endpoint."""
#     return {"status": "healthy"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import account_dashboard, stakeholder_details
from backend.app.db.base import Base
from backend.app.db.session import engine

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

@app.get("/")
def read_root():
    return {"message": "Welcome to the Account & Stakeholder API"}

# If running directly with python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
