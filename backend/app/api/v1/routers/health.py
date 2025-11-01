"""
Health check endpoint
"""

from fastapi import APIRouter, HTTPException
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns the health status of the application
    """
    return {
        "status": "healthy",
        "message": "Zyphron API is running"
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """
    Detailed health check including database and external services
    """
    checks = {
        "api": "operational",
        "database": "checking...",
        "docker": "checking...",
    }
    
    # In a real implementation, check each service
    try:
        from app.database import engine
        with engine.connect() as conn:
            checks["database"] = "operational"
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        checks["database"] = "unavailable"
    
    try:
        import docker
        client = docker.from_env()
        client.ping()
        checks["docker"] = "operational"
    except Exception as e:
        logger.error(f"Docker health check failed: {str(e)}")
        checks["docker"] = "unavailable"
    
    return {
        "status": "healthy" if all(v == "operational" for v in checks.values()) else "degraded",
        "checks": checks
    }
