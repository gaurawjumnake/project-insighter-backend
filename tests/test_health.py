"""
Unit Tests for Health Check Endpoint

Tests for:
- Happy path: Database is connected
- Unhappy path: Database connection fails
- Timeout handling
- Response schema validation
- HTTP status codes
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch, Mock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from main import app
from backend.core.schemas.health import HealthCheckResponse
from backend.core.services.health_service import HealthCheckService
from backend.db.session import get_db


# ============= FIXTURES =============

@pytest.fixture
def test_client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def mock_db_session():
    """Mock SQLAlchemy database session."""
    return MagicMock(spec=Session)


@pytest.fixture
def health_service(mock_db_session):
    """Health check service instance with mocked database."""
    return HealthCheckService(db=mock_db_session)


# ============= HELPER FUNCTIONS =============

def override_get_db(mock_session):
    """Override get_db dependency for testing."""
    def _override():
        return mock_session
    return _override


# ============= TESTS: Happy Path =============

@pytest.mark.asyncio
async def test_health_check_happy_path_db_connected(health_service, mock_db_session):
    """
    Test happy path: Database is connected and responsive.
    
    Expected:
    - status: "healthy"
    - database: "connected"
    - timestamp: valid ISO 8601 datetime
    - message: contains "OK"
    - No exceptions raised
    """
    # Mock successful database query
    mock_db_session.execute = MagicMock()
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (1,)
    mock_db_session.execute.return_value = mock_result
    
    # Call service
    response = await health_service.check_db_connectivity()
    
    # Assertions
    assert response.status == "healthy"
    assert response.database == "connected"
    assert isinstance(response.timestamp, datetime)
    assert "OK" in response.message or "latency" in response.message
    assert response.message is not None


# ============= TESTS: Unhappy Path - Connection Error =============

@pytest.mark.asyncio
async def test_health_check_db_connection_error(health_service, mock_db_session):
    """
    Test unhappy path: Database connection fails.
    
    Expected:
    - status: "unhealthy"
    - database: "disconnected"
    - message: contains error details
    """
    # Mock database connection error
    mock_db_session.execute = MagicMock(
        side_effect=OperationalError("could not connect to server", None, None)
    )
    
    # Call service
    response = await health_service.check_db_connectivity()
    
    # Assertions
    assert response.status == "unhealthy"
    assert response.database == "disconnected"
    assert isinstance(response.timestamp, datetime)
    assert "connection" in response.message.lower() or "failed" in response.message.lower()


# ============= TESTS: Timeout Handling =============

@pytest.mark.asyncio
async def test_health_check_db_timeout(health_service, mock_db_session):
    """
    Test timeout handling: Database query exceeds timeout.
    
    Expected:
    - status: "unhealthy"
    - database: "disconnected"
    - message: contains "timeout"
    """
    import asyncio
    
    # Mock slow database query (will timeout)
    async def slow_query(*args, **kwargs):
        await asyncio.sleep(10)  # Simulate slow response
    
    # Patch _execute_db_query to raise TimeoutError
    with patch.object(
        health_service,
        '_execute_db_query',
        side_effect=asyncio.TimeoutError()
    ):
        response = await health_service.check_db_connectivity()
    
    # Assertions
    assert response.status == "unhealthy"
    assert response.database == "disconnected"
    assert "timeout" in response.message.lower()


# ============= TESTS: Response Schema Validation =============

@pytest.mark.asyncio
async def test_health_check_response_schema_has_all_fields(health_service, mock_db_session):
    """
    Test that response schema contains all required fields.
    
    Expected:
    - All fields present (status, database, timestamp, message)
    - All fields have correct types
    """
    # Mock successful query
    mock_db_session.execute = MagicMock()
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (1,)
    mock_db_session.execute.return_value = mock_result
    
    # Call service
    response = await health_service.check_db_connectivity()
    
    # Verify all fields are present
    assert hasattr(response, 'status')
    assert hasattr(response, 'database')
    assert hasattr(response, 'timestamp')
    assert hasattr(response, 'message')
    
    # Verify types
    assert isinstance(response.status, str)
    assert isinstance(response.database, str)
    assert isinstance(response.timestamp, datetime)
    assert isinstance(response.message, str)
    
    # Verify enum values
    assert response.status in ["healthy", "unhealthy"]
    assert response.database in ["connected", "disconnected"]


# ============= TESTS: HTTP Endpoint =============

def test_health_endpoint_returns_200_when_healthy(test_client, mock_db_session):
    """
    Test HTTP endpoint: Returns 200 when database is healthy.
    
    Expected:
    - Status code: 200 OK
    - Response body: Valid HealthCheckResponse
    """
    # Mock database session
    mock_db_session.execute = MagicMock()
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (1,)
    mock_db_session.execute.return_value = mock_result
    
    # Override dependency
    app.dependency_overrides[get_db] = override_get_db(mock_db_session)
    
    try:
        # Make request
        response = test_client.get("/api/v1/health")
        
        # Assertions
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert data["database"] == "connected"
        assert "timestamp" in data
        assert "message" in data
        assert "OK" in data["message"] or "latency" in data["message"]
    
    finally:
        # Clean up overrides
        app.dependency_overrides.clear()


def test_health_endpoint_db_connection_error(test_client, mock_db_session):
    """
    Test HTTP endpoint: Returns appropriate response when database connection fails.
    
    Expected:
    - Status code: 200 (endpoint always returns 200, status in body indicates unhealthy)
    - Response body: status="unhealthy", database="disconnected"
    """
    # Mock database connection error
    mock_db_session.execute = MagicMock(
        side_effect=OperationalError("connection refused", None, None)
    )
    
    # Override dependency
    app.dependency_overrides[get_db] = override_get_db(mock_db_session)
    
    try:
        # Make request
        response = test_client.get("/api/v1/health")
        
        # Assertions
        assert response.status_code == 200  # Endpoint returns 200 always
        
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["database"] == "disconnected"
        assert "timestamp" in data
        assert "failed" in data["message"].lower() or "connection" in data["message"].lower()
    
    finally:
        # Clean up overrides
        app.dependency_overrides.clear()


# ============= TESTS: Response Content Type =============

def test_health_endpoint_content_type(test_client, mock_db_session):
    """
    Test HTTP endpoint: Returns JSON content type.
    
    Expected:
    - Content-Type: application/json
    """
    # Mock database
    mock_db_session.execute = MagicMock()
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (1,)
    mock_db_session.execute.return_value = mock_result
    
    # Override dependency
    app.dependency_overrides[get_db] = override_get_db(mock_db_session)
    
    try:
        # Make request
        response = test_client.get("/api/v1/health")
        
        # Assertions
        assert "application/json" in response.headers.get("content-type", "")
    
    finally:
        # Clean up overrides
        app.dependency_overrides.clear()


# ============= TESTS: OpenAPI Documentation =============

def test_health_endpoint_in_openapi_docs(test_client):
    """
    Test that health endpoint is documented in OpenAPI schema.
    
    Expected:
    - /api/v1/health endpoint present in OpenAPI spec
    - Proper description and response models
    """
    # Get OpenAPI schema
    response = test_client.get("/openapi.json")
    
    assert response.status_code == 200
    
    openapi_spec = response.json()
    
    # Check that health endpoint is documented
    assert "/api/v1/health" in openapi_spec["paths"]
    
    # Check GET method is documented
    path_spec = openapi_spec["paths"]["/api/v1/health"]
    assert "get" in path_spec
    
    # Check tags
    get_spec = path_spec["get"]
    assert "Health Check" in get_spec.get("tags", [])


# ============= TESTS: Error Scenarios =============

@pytest.mark.asyncio
async def test_health_check_generic_exception(health_service, mock_db_session):
    """
    Test handling of unexpected exceptions.
    
    Expected:
    - status: "unhealthy"
    - message: Contains error details
    - No crash/unhandled exception
    """
    # Mock generic exception
    mock_db_session.execute = MagicMock(
        side_effect=Exception("Unexpected error: DB server restarting")
    )
    
    # Call service - should not raise exception
    response = await health_service.check_db_connectivity()
    
    # Assertions
    assert response.status == "unhealthy"
    assert response.database == "disconnected"
    assert isinstance(response.message, str)
    assert len(response.message) > 0


# ============= TESTS: Timestamp Validation =============

@pytest.mark.asyncio
async def test_health_check_timestamp_is_recent(health_service, mock_db_session):
    """
    Test that timestamp in response is recent (within last minute).
    
    Expected:
    - Timestamp is within 1 minute of current time
    """
    from datetime import timedelta
    
    # Mock successful query
    mock_db_session.execute = MagicMock()
    mock_result = MagicMock()
    mock_result.fetchone.return_value = (1,)
    mock_db_session.execute.return_value = mock_result
    
    # Call service
    before_call = datetime.utcnow()
    response = await health_service.check_db_connectivity()
    after_call = datetime.utcnow()
    
    # Assertions
    assert before_call <= response.timestamp <= after_call + timedelta(seconds=1)


# ============= INTEGRATION TESTS =============

def test_health_endpoint_integration(test_client):
    """
    Integration test: Full request/response cycle.
    
    Tests:
    - Endpoint is accessible at correct URL
    - Returns valid JSON response
    - Schema is correct
    
    Note: This test uses actual database connection (or mock if provided).
    """
    # Make request to health endpoint
    response = test_client.get("/api/v1/health")
    
    # Should return 200 (endpoint always returns 200)
    assert response.status_code == 200
    
    # Should return JSON
    data = response.json()
    assert isinstance(data, dict)
    
    # Should have all required fields
    required_fields = ["status", "database", "timestamp", "message"]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
    
    # Validate enum values
    assert data["status"] in ["healthy", "unhealthy"]
    assert data["database"] in ["connected", "disconnected"]


# ============= COVERAGE TARGET: ≥95% =============
# Current coverage includes:
# - ✅ Happy path (database connected)
# - ✅ Connection error (OperationalError)
# - ✅ Timeout handling (asyncio.TimeoutError)
# - ✅ Generic exceptions
# - ✅ Schema validation (all fields, types, enums)
# - ✅ HTTP status codes
# - ✅ Content type verification
# - ✅ OpenAPI documentation
# - ✅ Timestamp validation
# - ✅ Integration test
#
# Expected coverage: >95% of health_service.py and health.py
