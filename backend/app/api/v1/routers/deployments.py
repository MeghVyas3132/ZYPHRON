"""
Deployment management endpoints
Create, update, delete, and manage deployments
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.models.deployment import Deployment, DeploymentStatus
from app.models.user import User
from app.schemas import (
    DeploymentCreate, DeploymentResponse, DeploymentDetailResponse,
    PaginationParams
)
from app.core.security import get_current_user

router = APIRouter(prefix="/deployments", tags=["deployments"])
logger = logging.getLogger(__name__)


@router.post("", response_model=DeploymentResponse, status_code=status.HTTP_201_CREATED)
async def create_deployment(
    deployment_data: DeploymentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new deployment
    """
    # Check if subdomain is already taken
    existing_subdomain = db.query(Deployment).filter(
        Deployment.subdomain == deployment_data.subdomain
    ).first()
    
    if existing_subdomain:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subdomain is already taken"
        )
    
    # Create new deployment
    new_deployment = Deployment(
        user_id=current_user.id,
        project_name=deployment_data.project_name,
        subdomain=deployment_data.subdomain,
        full_url=f"{deployment_data.subdomain}.zyphron.space",
        repo_url=deployment_data.repo_url,
        repo_branch=deployment_data.repo_branch,
        repo_type=deployment_data.repo_type,
        status=DeploymentStatus.DETECTING
    )
    
    db.add(new_deployment)
    db.commit()
    db.refresh(new_deployment)
    
    logger.info(f"New deployment created: {new_deployment.id} for user {current_user.id}")
    
    # TODO: Trigger deployment pipeline asynchronously
    
    return new_deployment


@router.get("", response_model=dict)
async def list_deployments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    List all deployments for current user
    """
    deployments = db.query(Deployment).filter(
        Deployment.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    total = db.query(Deployment).filter(
        Deployment.user_id == current_user.id
    ).count()
    
    return {
        "items": deployments,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_more": (skip + limit) < total
    }


@router.get("/{deployment_id}", response_model=DeploymentDetailResponse)
async def get_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get deployment details by ID
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
    
    return deployment


@router.delete("/{deployment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a deployment
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
    
    db.delete(deployment)
    db.commit()
    
    logger.info(f"Deployment deleted: {deployment_id}")
    
    return None


@router.post("/{deployment_id}/rollback", response_model=dict)
async def rollback_deployment(
    deployment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Rollback a deployment to previous version
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
    
    # TODO: Implement rollback logic
    
    return {
        "message": "Rollback initiated",
        "deployment_id": deployment_id
    }
