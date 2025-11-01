"""
Monitoring and health check endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.database import get_db
from app.models.deployment import Deployment, MonitoringLog
from app.models.user import User
from app.schemas import HealthCheckResponse, MonitoringMetrics
from app.core.security import get_current_user

router = APIRouter(prefix="/monitoring", tags=["monitoring"])
logger = logging.getLogger(__name__)


@router.get("/deployments/{deployment_id}/uptime", response_model=dict)
async def get_deployment_uptime(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get uptime metrics for a deployment
    """
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id,
        Deployment.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    # Get monitoring logs
    logs = db.query(MonitoringLog).filter(
        MonitoringLog.deployment_id == deployment_id,
        MonitoringLog.check_type == "uptime"
    ).order_by(MonitoringLog.checked_at.desc()).limit(100).all()
    
    total_checks = len(logs)
    failed_checks = sum(1 for log in logs if log.status == "failed")
    success_rate = ((total_checks - failed_checks) / total_checks * 100) if total_checks > 0 else 100
    
    return {
        "deployment_id": deployment_id,
        "uptime_percentage": deployment.uptime_percentage,
        "total_checks": total_checks,
        "failed_checks": failed_checks,
        "success_rate": success_rate,
        "last_check": logs[0].checked_at if logs else None
    }


@router.get("/deployments/{deployment_id}/health-checks", response_model=dict)
async def get_health_checks(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500)
):
    """
    Get recent health checks for a deployment
    """
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id,
        Deployment.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    checks = db.query(MonitoringLog).filter(
        MonitoringLog.deployment_id == deployment_id,
        MonitoringLog.check_type == "health"
    ).order_by(MonitoringLog.checked_at.desc()).limit(limit).all()
    
    return {
        "deployment_id": deployment_id,
        "checks": checks,
        "total": len(checks)
    }


@router.get("/deployments/{deployment_id}/performance", response_model=dict)
async def get_performance_metrics(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=500)
):
    """
    Get performance metrics for a deployment
    """
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id,
        Deployment.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    logs = db.query(MonitoringLog).filter(
        MonitoringLog.deployment_id == deployment_id,
        MonitoringLog.check_type == "performance"
    ).order_by(MonitoringLog.checked_at.desc()).limit(limit).all()
    
    # Calculate averages
    avg_response_time = sum(log.response_time_ms for log in logs if log.response_time_ms) / len(logs) if logs else 0
    avg_cpu = sum(log.cpu_usage_percent for log in logs if log.cpu_usage_percent) / len(logs) if logs else 0
    avg_memory = sum(log.memory_usage_mb for log in logs if log.memory_usage_mb) / len(logs) if logs else 0
    
    return {
        "deployment_id": deployment_id,
        "avg_response_time_ms": avg_response_time,
        "avg_cpu_percent": avg_cpu,
        "avg_memory_mb": avg_memory,
        "metrics_count": len(logs),
        "recent_metrics": logs
    }


@router.post("/deployments/{deployment_id}/check", status_code=status.HTTP_202_ACCEPTED)
async def trigger_health_check(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Manually trigger a health check for a deployment
    """
    deployment = db.query(Deployment).filter(
        Deployment.id == deployment_id,
        Deployment.user_id == current_user.id
    ).first()
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    # TODO: Trigger health check asynchronously
    
    return {
        "message": "Health check initiated",
        "deployment_id": deployment_id
    }
