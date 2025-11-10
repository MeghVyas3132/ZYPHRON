"""
Zyphron Backend - Main FastAPI Application
Production-ready deployment platform for any repository
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings
from app.core.security import init_security
from app.api.v1.routers import health, users, deployments, monitoring, subdomain
from app.database import engine, Base, get_db
from app.init_db import init_database
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting Zyphron Backend...")
    
    # Initialize database tables
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables initialized")
    
    # Initialize security
    init_security()
    logger.info("✅ Security initialized")
    
    # Initialize database with test data
    init_database()
    logger.info("✅ Database seeding complete")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Zyphron Backend...")
    logger.info("✅ Cleanup complete")


# Create FastAPI app
app = FastAPI(
    title="Zyphron API",
    description="Production-ready deployment platform for any repository",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    """Handle database exceptions"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(deployments.router, prefix="/api/v1", tags=["Deployments"])
app.include_router(monitoring.router, prefix="/api/v1", tags=["Monitoring"])
app.include_router(subdomain.router, prefix="/api/v1", tags=["Subdomains"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Zyphron API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
