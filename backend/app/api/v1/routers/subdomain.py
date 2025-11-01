"""
Subdomain management endpoints
Check availability, manage subdomains
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models.deployment import Deployment
from app.models.subdomain import Subdomain
from app.models.user import User
from app.schemas import (
    SubdomainAvailabilityRequest, SubdomainAvailabilityResponse,
    SubdomainResponse
)
from app.core.security import get_current_user

router = APIRouter(prefix="/subdomains", tags=["subdomains"])
logger = logging.getLogger(__name__)


@router.post("/check-availability", response_model=SubdomainAvailabilityResponse)
async def check_subdomain_availability(
    request: SubdomainAvailabilityRequest,
    db: Session = Depends(get_db)
):
    """
    Check if a subdomain is available
    """
    subdomain = request.subdomain.lower().replace(" ", "-")
    
    # Validate subdomain format
    if not _is_valid_subdomain(subdomain):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid subdomain format"
        )
    
    # Check if subdomain exists
    existing = db.query(Deployment).filter(
        Deployment.subdomain == subdomain
    ).first()
    
    if existing:
        suggestions = _generate_suggestions(subdomain, db)
        return SubdomainAvailabilityResponse(
            subdomain=subdomain,
            is_available=False,
            suggestions=suggestions,
            message=f"Subdomain '{subdomain}' is already taken"
        )
    
    return SubdomainAvailabilityResponse(
        subdomain=subdomain,
        is_available=True,
        message=f"Subdomain '{subdomain}' is available"
    )


@router.get("/{deployment_id}", response_model=SubdomainResponse)
async def get_deployment_subdomain(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get subdomain for a deployment
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
    
    subdomain = db.query(Subdomain).filter(
        Subdomain.deployment_id == deployment_id
    ).first()
    
    if not subdomain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subdomain not found"
        )
    
    return subdomain


def _is_valid_subdomain(subdomain: str) -> bool:
    """
    Validate subdomain format
    - 3-63 characters
    - Only lowercase letters, numbers, and hyphens
    - Cannot start or end with hyphen
    """
    import re
    
    pattern = r"^[a-z0-9]([a-z0-9-]{1,61}[a-z0-9])?$"
    return bool(re.match(pattern, subdomain)) and len(subdomain) <= 63


def _generate_suggestions(subdomain: str, db: Session) -> list:
    """
    Generate available subdomain suggestions
    """
    suggestions = []
    
    # Try adding numbers
    for i in range(1, 10):
        candidate = f"{subdomain}{i}"
        if not db.query(Deployment).filter(Deployment.subdomain == candidate).first():
            suggestions.append(candidate)
            if len(suggestions) >= 5:
                break
    
    # Try adding prefixes/suffixes
    if len(suggestions) < 5:
        for suffix in ["app", "dev", "prod", "api", "web"]:
            candidate = f"{subdomain}-{suffix}"
            if not db.query(Deployment).filter(Deployment.subdomain == candidate).first():
                suggestions.append(candidate)
                if len(suggestions) >= 5:
                    break
    
    return suggestions[:5]
