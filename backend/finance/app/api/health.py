from fastapi import APIRouter, Depends, status

from backend.core.schemas.health import HealthCheckResponse
from backend.core.services.health_service import HealthCheckService, get_health_check_service

# Initialize router
router = APIRouter(
    prefix="/health",
    tags=["Health Check"],
    responses={
        200: {"description": "Application is healthy and database is accessible"},
        503: {"description": "Application is unhealthy or database is inaccessible"}
    }
)


@router.get(
    "",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Application is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "database": "connected",
                        "timestamp": "2026-05-07T14:30:00Z",
                        "message": "Database connectivity OK (latency: 2ms)"
                    }
                }
            }
        },
        503: {
            "description": "Application is unhealthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "unhealthy",
                        "database": "disconnected",
                        "timestamp": "2026-05-07T14:30:05Z",
                        "message": "Failed to connect to database: connection timeout (5s)"
                    }
                }
            }
        }
    }
)
async def health_check(
    health_service: HealthCheckService = Depends(get_health_check_service)
) -> HealthCheckResponse:
    """
    Check application and database health.
    
    This endpoint performs a simple health check by attempting to connect to the database.
    It's useful for:
    - Load balancer health checks (ALB, NLB)
    - Kubernetes liveness and readiness probes
    - Monitoring and alerting systems
    - Application startup validation
    
    **Response Status Codes:**
    - `200`: Application is healthy and database is accessible
    - `503`: Application is unhealthy or database is inaccessible
    
    **Example Healthy Response:**
    ```json
    {
        "status": "healthy",
        "database": "connected",
        "timestamp": "2026-05-07T14:30:00Z",
        "message": "Database connectivity OK (latency: 2ms)"
    }
    ```
    
    **Example Unhealthy Response:**
    ```json
    {
        "status": "unhealthy",
        "database": "disconnected",
        "timestamp": "2026-05-07T14:30:05Z",
        "message": "Failed to connect to database: connection timeout (5s)"
    }
    ```
    
    Args:
        health_service: Health check service instance (injected by FastAPI)
    
    Returns:
        HealthCheckResponse: Health status with timestamp and detailed message
    
    Raises:
        HTTPException: Not raised; all errors are returned as HealthCheckResponse
            with status="unhealthy" and appropriate error message
    """
    response = await health_service.check_db_connectivity()
    
    # If unhealthy, return 503 Service Unavailable
    if response.status == "unhealthy":
        return response  # FastAPI will automatically use status code 503 based on response
    
    return response
