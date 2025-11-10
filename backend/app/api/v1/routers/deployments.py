"""
Deployment management endpoints
Create, update, delete, and manage deployments
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging
import httpx
import os

from app.database import get_db
from app.models.deployment import Deployment, DeploymentStatus
from app.models.user import User
from app.schemas import (
    DeploymentCreate, DeploymentResponse, DeploymentDetailResponse,
    PaginationParams, PaginatedResponse
)
from app.core.security import get_current_user

router = APIRouter(prefix="/deployments", tags=["deployments"])
logger = logging.getLogger(__name__)


async def get_test_user(db: Session = Depends(get_db)) -> User:
    """Get or create test user for development/testing"""
    test_user = db.query(User).filter(User.id == 1).first()
    if not test_user:
        from app.core.security import hash_password
        test_user = User(
            id=1,
            email="test@zyphron.local",
            username="testuser",
            full_name="Test User",
            hashed_password=hash_password("testpass123"),
            is_active=True,
            is_verified=True,
            role="user"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        logger.info("Created test user with ID: 1")
    return test_user


@router.post("", response_model=DeploymentResponse, status_code=status.HTTP_201_CREATED)
async def create_deployment(
    deployment_data: DeploymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_test_user)
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
    
    # Trigger Jenkins pipeline
    try:
        await trigger_jenkins_pipeline(new_deployment)
    except Exception as e:
        logger.error(f"Failed to trigger Jenkins pipeline: {str(e)}")
    
    return new_deployment


async def trigger_jenkins_pipeline(deployment: Deployment):
    """Trigger Jenkins pipeline for deployment"""
    jenkins_url = os.getenv("JENKINS_URL", "http://zyphron_jenkins:8080")
    jenkins_token = os.getenv("JENKINS_TOKEN", "")
    
    pipeline_params = {
        "DEPLOYMENT_ID": str(deployment.id),
        "REPO_URL": deployment.repo_url,
        "REPO_BRANCH": deployment.repo_branch,
        "PROJECT_NAME": deployment.project_name,
        "SUBDOMAIN": deployment.subdomain,
        "REPO_TYPE": deployment.repo_type,
    }
    
    try:
        async with httpx.AsyncClient() as client:
            # Build Jenkins job trigger URL
            job_url = f"{jenkins_url}/job/zyphron-deploy/buildWithParameters"
            
            response = await client.post(job_url, params=pipeline_params)
            response.raise_for_status()
            
            logger.info(f"Jenkins pipeline triggered for deployment {deployment.id}")
    except Exception as e:
        logger.error(f"Failed to trigger Jenkins pipeline: {str(e)}")


@router.get("", response_model=PaginatedResponse)
async def list_deployments(
    current_user: User = Depends(get_test_user),
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
    
    # Convert to response models
    deployment_responses = [DeploymentResponse.model_validate(d) for d in deployments]
    
    return PaginatedResponse(
        items=deployment_responses,
        total=total,
        skip=skip,
        limit=limit,
        has_more=(skip + limit) < total
    )


@router.get("/{deployment_id}", response_model=DeploymentDetailResponse)
async def get_deployment(
    deployment_id: int,
    current_user: User = Depends(get_test_user),
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
    current_user: User = Depends(get_test_user),
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


@router.post("/{deployment_id}/update-status", response_model=DeploymentResponse)
async def update_deployment_status(
    deployment_id: int,
    status: str = Query(...),
    container_id: str = Query(None),
    container_port: int = Query(None),
    deployed_at: str = Query(None),
    deployment_logs: str = Query(None),
    error_logs: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Update deployment status (called by Jenkins after deployment)
    """
    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    
    if not deployment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deployment not found"
        )
    
    # Update deployment status
    deployment.status = status
    if container_id:
        deployment.container_ids = [container_id] if not deployment.container_ids else deployment.container_ids + [container_id]
    if container_port:
        deployment.container_port = container_port
    if deployment_logs:
        deployment.deployment_logs = deployment_logs
    if error_logs:
        deployment.error_logs = error_logs
    
    db.commit()
    db.refresh(deployment)
    
    logger.info(f"Deployment {deployment_id} status updated to: {status}")
    
    return deployment


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
