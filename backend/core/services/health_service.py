"""
Health Check Service

Service layer for database connectivity health checks.
Provides the core logic for checking database connectivity with proper error handling and logging.
"""

import asyncio
from datetime import datetime
from typing import Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends

from backend.core.schemas.health import HealthCheckResponse
from backend.db.session import get_db
from backend.doc_insighter.tools.app_logger import Logger

# Initialize logger
logger = Logger()


class HealthCheckService:
    """Service for performing health checks on database connectivity."""
    
    def __init__(self, db: Session):
        """
        Initialize health check service.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.db_timeout = 5  # seconds
    
    async def check_db_connectivity(self) -> HealthCheckResponse:
        """
        Check database connectivity with timeout handling.
        
        Attempts to execute a simple SELECT 1 query on the database.
        If successful, returns healthy status; otherwise returns unhealthy.
        
        Returns:
            HealthCheckResponse: Schema with status, database, timestamp, and message
            
        Example:
            >>> service = HealthCheckService(db_session)
            >>> response = await service.check_db_connectivity()
            >>> print(response.status)
            'healthy'
        """
        try:
            logger.log_info("Starting database connectivity check")
            
            # Execute simple query with timeout
            result, latency_ms = await self._execute_db_query()
            
            if result:
                logger.log_info(f"Database connectivity check passed (latency: {latency_ms}ms)")
                return HealthCheckResponse(
                    status="healthy",
                    database="connected",
                    timestamp=datetime.utcnow(),
                    message=f"Database connectivity OK (latency: {latency_ms}ms)"
                )
            else:
                logger.log_warning("Database connectivity check failed: no response from query")
                return HealthCheckResponse(
                    status="unhealthy",
                    database="disconnected",
                    timestamp=datetime.utcnow(),
                    message="Database connectivity check failed: no response from query"
                )
        
        except asyncio.TimeoutError:
            logger.log_error(f"Database connectivity check timed out (timeout: {self.db_timeout}s)")
            return HealthCheckResponse(
                status="unhealthy",
                database="disconnected",
                timestamp=datetime.utcnow(),
                message=f"Failed to connect to database: connection timeout ({self.db_timeout}s)"
            )
        
        except Exception as e:
            error_msg = str(e)
            logger.log_error(f"Database connectivity check failed: {error_msg}")
            return HealthCheckResponse(
                status="unhealthy",
                database="disconnected",
                timestamp=datetime.utcnow(),
                message=f"Failed to connect to database: {error_msg}"
            )
    
    async def _execute_db_query(self) -> Tuple[bool, int]:
        """
        Execute a simple SELECT 1 query to test database connectivity.
        
        This is a low-overhead test that validates the database connection
        without retrieving large amounts of data.
        
        Returns:
            Tuple[bool, int]: (success_flag, latency_in_ms)
            
        Raises:
            asyncio.TimeoutError: If query exceeds timeout threshold
            Exception: Any database connection error
        """
        import time
        
        start_time = time.perf_counter()
        
        try:
            # Execute query with timeout wrapper
            await asyncio.wait_for(
                asyncio.to_thread(
                    self._sync_db_query
                ),
                timeout=self.db_timeout
            )
            
            end_time = time.perf_counter()
            latency_ms = int((end_time - start_time) * 1000)
            
            return True, latency_ms
        
        except asyncio.TimeoutError:
            raise  # Re-raise timeout errors
        
        except Exception as e:
            raise  # Re-raise other exceptions for caller to handle
    
    def _sync_db_query(self) -> None:
        """
        Synchronous database query execution.
        
        Uses SQLAlchemy to execute SELECT 1 on the database.
        This method is wrapped in asyncio.to_thread for async compatibility.
        
        Raises:
            Exception: Any database error
        """
        try:
            # Execute simple SELECT 1 query
            result = self.db.execute(text("SELECT 1"))
            result.fetchone()
        except Exception as e:
            logger.log_error(f"Sync DB query failed: {str(e)}")
            raise


def get_health_check_service(db: Session = Depends(get_db)) -> HealthCheckService:
    """
    Factory function to create HealthCheckService instance.
    
    Used for dependency injection in FastAPI routes.
    
    Args:
        db: SQLAlchemy database session from get_db() dependency
        
    Returns:
        HealthCheckService: Initialized service instance
    """
    return HealthCheckService(db=db)
