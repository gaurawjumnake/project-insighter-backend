"""
Pytest configuration and shared fixtures for smoke tests.
Provides mocks for external dependencies (S3, LLM, Database).
"""

import pytest
import json
from unittest.mock import Mock, MagicMock, patch
from uuid import uuid4
from typing import Dict, Any, Generator


# ============================================================================
# MOCK CREDENTIALS & CONFIGURATION
# ============================================================================

@pytest.fixture(scope="session")
def test_config():
    """Test configuration with safe defaults."""
    return {
        "project_id": str(uuid4()),
        "account_id": str(uuid4()),
        "pe_id": str(uuid4()),
        "aws_region": "us-east-1",
        "s3_bucket": "test-insights-bucket",
        "openai_api_key": "test-key-12345",
    }


# ============================================================================
# DATABASE FIXTURES
# ============================================================================

@pytest.fixture
def mock_db_session():
    """Mocked SQLAlchemy database session."""
    mock_session = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = None
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.rollback.return_value = None
    mock_session.close.return_value = None
    return mock_session


# ============================================================================
# S3 STORAGE FIXTURES
# ============================================================================

@pytest.fixture
def mock_s3_client():
    """Mocked AWS S3 client."""
    client = MagicMock()
    client.put_object.return_value = {"ETag": "mock-etag-123"}
    client.get_object.return_value = {
        "Body": MagicMock(
            read=lambda: json.dumps({
                "entity_type": "project",
                "entity_id": str(uuid4()),
                "entity_name": "Test Project",
                "financial_metrics": {},
                "documents": [],
                "warnings": []
            }).encode("utf-8")
        )
    }
    return client


@pytest.fixture
def mock_s3_storage(mock_s3_client):
    """Fixture that patches S3 storage utilities."""
    with patch("backend.utitlites.s3_storage.upload_data_to_s3") as mock_upload, \
         patch("backend.utitlites.s3_storage.download_data_from_s3") as mock_download:
        
        mock_upload.return_value = "s3://test-bucket/test-key.json"
        mock_download.return_value = {
            "entity_type": "project",
            "entity_id": str(uuid4()),
            "entity_name": "Test Project",
            "financial_metrics": {
                "total_revenue": 100000.0,
                "total_cost": 75000.0
            },
            "documents": [
                {"type": "sow", "count": 1},
                {"type": "wsr", "count": 2}
            ],
            "warnings": []
        }
        
        yield {
            "upload": mock_upload,
            "download": mock_download,
            "client": mock_s3_client
        }


# ============================================================================
# LLM & CREWAI FIXTURES
# ============================================================================

@pytest.fixture
def mock_llm():
    """Mocked LLM client (Azure OpenAI)."""
    llm = MagicMock()
    llm.model = "gpt-4o"
    llm.call.return_value = "Mock LLM response"
    return llm


@pytest.fixture
def mock_crew_task():
    """Mocked CrewAI Task."""
    task = MagicMock()
    task.output = "Mock task output"
    task.output.raw = "Raw mock output"
    return task


@pytest.fixture
def mock_crew_agent():
    """Mocked CrewAI Agent."""
    agent = MagicMock()
    agent.role = "Test Agent"
    agent.goal = "Test Goal"
    return agent


@pytest.fixture
def mock_crew_execution():
    """Mocked CrewAI Crew execution result."""
    result = MagicMock()
    result.raw = json.dumps({
        "insights": "Mock insights from crew execution",
        "analysis": {
            "status": "success",
            "entity_type": "project",
            "timestamp": "2026-05-07T10:00:00Z"
        }
    })
    result.output = result.raw
    return result


# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_project_data() -> Dict[str, Any]:
    """Sample project data for testing."""
    return {
        "entity_type": "project",
        "entity_id": str(uuid4()),
        "entity_name": "Cloud Migration Project",
        "account_id": str(uuid4()),
        "financial_metrics": {
            "total_revenue": 500000.0,
            "total_cost": 350000.0,
            "profitability": 150000.0,
            "margin_percentage": 30.0
        },
        "operational_metrics": {
            "status": "in_progress",
            "progress_percentage": 65.5,
            "on_schedule": True,
            "on_budget": True
        },
        "documents": [
            {
                "type": "sow",
                "count": 1,
                "extracted_insights": {
                    "scope": "Cloud infrastructure migration",
                    "deliverables": ["Design", "Implementation", "Testing"],
                    "timeline": "6 months"
                }
            },
            {
                "type": "wsr",
                "count": 5,
                "latest_metrics": {
                    "progress": "65%",
                    "risks": ["Resource availability"],
                    "blockers": []
                }
            }
        ],
        "warnings": [],
        "data_quality": "high"
    }


@pytest.fixture
def sample_account_data() -> Dict[str, Any]:
    """Sample account data for testing."""
    return {
        "entity_type": "account",
        "entity_id": str(uuid4()),
        "entity_name": "Acme Corp",
        "financial_metrics": {
            "total_revenue": 2000000.0,
            "total_cost": 1400000.0,
            "profitability": 600000.0,
            "active_projects": 5,
            "average_margin": 30.0
        },
        "projects": [
            {
                "project_id": str(uuid4()),
                "project_name": "Project A",
                "status": "completed",
                "margin": 25.0
            },
            {
                "project_id": str(uuid4()),
                "project_name": "Project B",
                "status": "in_progress",
                "margin": 35.0
            }
        ],
        "warnings": [],
        "data_quality": "high"
    }


@pytest.fixture
def sample_pe_data() -> Dict[str, Any]:
    """Sample private equity data for testing."""
    return {
        "entity_type": "private_equity",
        "entity_id": str(uuid4()),
        "entity_name": "Tech Holdings Fund I",
        "portfolio_metrics": {
            "total_companies": 5,
            "total_aum": 50000000.0,
            "avg_irr": 20.5,
            "active_deals": 2
        },
        "companies": [
            {
                "company_id": str(uuid4()),
                "company_name": "Company A",
                "investment_date": "2024-01-15",
                "valuation": 10000000.0
            }
        ],
        "warnings": [],
        "data_quality": "high"
    }


# ============================================================================
# PATCHING FIXTURES
# ============================================================================

@pytest.fixture
def patch_external_dependencies():
    """Patches all external dependencies for isolated testing."""
    patches = {}
    
    # Patch S3
    with patch("backend.utitlites.s3_storage.upload_data_to_s3") as mock_upload, \
         patch("backend.utitlites.s3_storage.download_data_from_s3") as mock_download, \
         patch("backend.utitlites.llm_models.llm") as mock_llm, \
         patch("backend.db.session.SessionLocal") as mock_session_factory:
        
        # Configure mocks
        mock_upload.return_value = "s3://test-bucket/test-key.json"
        mock_download.return_value = {
            "entity_type": "project",
            "entity_id": str(uuid4()),
            "entity_name": "Test Project",
            "financial_metrics": {}
        }
        mock_llm.model = "gpt-4o"
        mock_session = MagicMock()
        mock_session_factory.return_value = mock_session
        
        patches = {
            "s3_upload": mock_upload,
            "s3_download": mock_download,
            "llm": mock_llm,
            "db_session_factory": mock_session_factory,
            "db_session": mock_session
        }
        
        yield patches


# ============================================================================
# UTILITY FIXTURES
# ============================================================================

@pytest.fixture
def capture_logs(caplog):
    """Captures log messages for assertion."""
    import logging
    caplog.set_level(logging.DEBUG)
    return caplog


@pytest.fixture
def timer():
    """Simple timer for performance testing."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        @property
        def elapsed(self) -> float:
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return 0.0
    
    return Timer()
