"""
Database initialization and seeding
Creates default test data for development
"""

import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

logger = logging.getLogger(__name__)


def create_test_user(db: Session):
    """Create a default test user for development"""
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.email == "test@zyphron.local").first()
        if existing_user:
            logger.info("Test user already exists")
            return existing_user
        
        # Create test user
        test_user = User(
            email="test@zyphron.local",
            username="testuser",
            full_name="Test User",
            hashed_password=hash_password("testpass123"),
            is_active=True,
            is_verified=True,
            role="user",
            avatar_url=None,
            bio="Default test user for development"
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        logger.info(f"✅ Test user created with ID: {test_user.id}")
        return test_user
    except Exception as e:
        logger.error(f"Error creating test user: {str(e)}")
        db.rollback()
        return None


def init_database():
    """Initialize database with default data"""
    db = SessionLocal()
    try:
        create_test_user(db)
        logger.info("✅ Database initialization complete")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
    finally:
        db.close()
