"""
Application configuration settings
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "postgresql://zyphron:zyphron@localhost:5432/zyphron"
    DATABASE_ECHO: bool = False
    
    # Security
    JWT_SECRET_KEY: str = "your-jwt-secret-key-here"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Docker
    DOCKER_HOST: str = "unix:///var/run/docker.sock"
    CONTAINER_REGISTRY: str = "docker.io"
    
    # Email
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SENDER_EMAIL: str = "noreply@zyphron.space"
    
    # Application URLs
    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Deployment
    DEPLOYMENT_DIR: str = "/app/deployments"
    TEMP_BUILD_DIR: str = "/tmp/zyphron-builds"
    MAX_REPO_SIZE_MB: int = 1000
    DEPLOYMENT_TIMEOUT_SECONDS: int = 3600
    
    # Monitoring
    ENABLE_MONITORING: bool = True
    HEALTH_CHECK_INTERVAL: int = 30
    UPTIME_CHECK_INTERVAL: int = 60
    
    # Nginx
    NGINX_CONFIG_DIR: str = "/etc/nginx/sites-available"
    MAIN_DOMAIN: str = "zyphron.space"
    MAIN_DOMAIN_IP: str = "127.0.0.1"
    
    # SSL/TLS
    CERTBOT_EMAIL: str = "admin@zyphron.space"
    SSL_CERT_DIR: str = "/etc/letsencrypt/live"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "/var/log/zyphron/backend.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
