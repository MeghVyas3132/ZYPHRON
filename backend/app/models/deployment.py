"""
Deployment model for database
Tracks all deployments made by users
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

from app.database import Base


class DeploymentStatus(str, PyEnum):
    """Deployment status enum"""
    PENDING = "pending"
    DETECTING = "detecting"
    BUILDING = "building"
    TESTING = "testing"
    DEPLOYING = "deploying"
    LIVE = "live"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class Deployment(Base):
    """Deployment model tracking all user deployments"""
    
    __tablename__ = "deployments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    
    # Deployment metadata
    project_name = Column(String(255), nullable=False)
    subdomain = Column(String(255), unique=True, index=True, nullable=False)
    full_url = Column(String(500), nullable=True)
    
    # Repository info
    repo_url = Column(String(500), nullable=False)
    repo_branch = Column(String(100), default="main", nullable=False)
    repo_type = Column(String(50), nullable=False)  # github, gitlab, gitea, etc.
    
    # Detection info
    detected_languages = Column(JSON, nullable=True)  # List of detected languages
    detected_frameworks = Column(JSON, nullable=True)  # List of detected frameworks
    detected_databases = Column(JSON, nullable=True)  # List of detected databases
    detected_services = Column(JSON, nullable=True)  # List of other services
    
    # Deployment configuration
    status = Column(String(50), default=DeploymentStatus.PENDING, nullable=False)
    container_ids = Column(JSON, nullable=True)  # Docker container IDs
    docker_compose_version = Column(String(50), nullable=True)
    
    # Environment variables (encrypted in production)
    env_variables = Column(JSON, nullable=True)
    env_required = Column(JSON, nullable=True)  # List of required env variables
    
    # Logs and monitoring
    deployment_logs = Column(Text, nullable=True)
    error_logs = Column(Text, nullable=True)
    
    # Performance metrics
    build_duration_seconds = Column(Float, nullable=True)
    test_duration_seconds = Column(Float, nullable=True)
    deployment_duration_seconds = Column(Float, nullable=True)
    
    # Uptime tracking
    uptime_percentage = Column(Float, default=100.0, nullable=False)
    last_health_check = Column(DateTime, nullable=True)
    downtime_seconds = Column(Integer, default=0, nullable=False)
    
    # Dates
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deployed_at = Column(DateTime, nullable=True)
    last_rollback_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="deployments")
    monitoring_logs = relationship("MonitoringLog", back_populates="deployment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Deployment(id={self.id}, project={self.project_name}, subdomain={self.subdomain}, status={self.status})>"


class MonitoringLog(Base):
    """Monitoring and health check logs"""
    
    __tablename__ = "monitoring_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    deployment_id = Column(Integer, ForeignKey("deployments.id"), index=True, nullable=False)
    
    # Check type
    check_type = Column(String(50), nullable=False)  # health, uptime, performance, error
    status = Column(String(50), nullable=False)  # success, failed, timeout
    
    # Response info
    response_time_ms = Column(Float, nullable=True)
    status_code = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Container metrics
    cpu_usage_percent = Column(Float, nullable=True)
    memory_usage_mb = Column(Float, nullable=True)
    memory_limit_mb = Column(Float, nullable=True)
    
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    deployment = relationship("Deployment", back_populates="monitoring_logs")
    
    def __repr__(self):
        return f"<MonitoringLog(id={self.id}, deployment_id={self.deployment_id}, check_type={self.check_type}, status={self.status})>"
