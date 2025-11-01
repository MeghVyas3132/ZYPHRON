"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict
from datetime import datetime


# ============ User Schemas ============

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(UserResponse):
    last_login: Optional[datetime]
    avatar_url: Optional[str]
    bio: Optional[str]


# ============ Authentication Schemas ============

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ============ Deployment Schemas ============

class DeploymentBase(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=255)
    subdomain: str = Field(..., min_length=1, max_length=255)
    repo_url: str
    repo_branch: str = "main"


class DeploymentCreate(DeploymentBase):
    repo_type: str = "github"


class DeploymentUpdate(BaseModel):
    project_name: Optional[str] = None
    env_variables: Optional[Dict[str, str]] = None


class DeploymentResponse(DeploymentBase):
    id: int
    user_id: int
    status: str
    full_url: Optional[str]
    uptime_percentage: float
    created_at: datetime
    deployed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class DeploymentDetailResponse(DeploymentResponse):
    detected_languages: Optional[List[str]]
    detected_frameworks: Optional[List[str]]
    detected_databases: Optional[List[str]]
    container_ids: Optional[List[str]]
    deployment_logs: Optional[str]
    error_logs: Optional[str]
    build_duration_seconds: Optional[float]
    deployment_duration_seconds: Optional[float]


# ============ Environment Variables Schemas ============

class EnvVarRequest(BaseModel):
    deployment_id: int
    env_variables: Dict[str, str]


class EnvVarResponse(BaseModel):
    deployment_id: int
    env_required: List[str]
    message: str


# ============ Monitoring Schemas ============

class HealthCheckResponse(BaseModel):
    deployment_id: int
    status: str  # success, failed, timeout
    response_time_ms: float
    status_code: Optional[int]
    checked_at: datetime
    
    class Config:
        from_attributes = True


class MonitoringMetrics(BaseModel):
    deployment_id: int
    uptime_percentage: float
    total_checks: int
    failed_checks: int
    cpu_usage_percent: Optional[float]
    memory_usage_mb: Optional[float]
    average_response_time_ms: Optional[float]


# ============ Subdomain Schemas ============

class SubdomainAvailabilityRequest(BaseModel):
    subdomain: str = Field(..., min_length=1, max_length=255)


class SubdomainAvailabilityResponse(BaseModel):
    subdomain: str
    is_available: bool
    suggestions: Optional[List[str]] = None
    message: str


class SubdomainResponse(BaseModel):
    id: int
    subdomain: str
    full_domain: str
    is_active: bool
    ssl_enabled: bool
    ssl_cert_expires_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============ Error Response Schemas ============

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============ Pagination Schemas ============

class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)


class PaginatedResponse(BaseModel):
    items: List
    total: int
    skip: int
    limit: int
    has_more: bool
