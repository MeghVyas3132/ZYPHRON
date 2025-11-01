"""
Subdomain model for tracking reserved subdomains
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Subdomain(Base):
    """Subdomain reservation and tracking"""
    
    __tablename__ = "subdomains"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    deployment_id = Column(Integer, ForeignKey("deployments.id"), index=True, nullable=False)
    
    subdomain = Column(String(255), unique=True, index=True, nullable=False)
    full_domain = Column(String(500), nullable=False)  # e.g., app1.zyphron.space
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # SSL/TLS
    ssl_enabled = Column(Boolean, default=True, nullable=False)
    ssl_cert_issued_at = Column(DateTime, nullable=True)
    ssl_cert_expires_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Subdomain(id={self.id}, subdomain={self.subdomain}, full_domain={self.full_domain})>"
