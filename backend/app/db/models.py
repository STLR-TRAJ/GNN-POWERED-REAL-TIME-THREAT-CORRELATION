"""
Database models for KRSN-RT2I Platform.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.db.database import Base

# Enums
class ThreatSeverity(enum.Enum):
    """Threat severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IndicatorType(enum.Enum):
    """Types of threat indicators."""
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    FILE_HASH = "file_hash"
    EMAIL = "email"

class AlertStatus(enum.Enum):
    """Alert status values."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"

# Models
class ThreatIndicator(Base):
    """Threat indicator model."""
    __tablename__ = "threat_indicators"
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String(255), nullable=False, index=True)
    type = Column(Enum(IndicatorType), nullable=False)
    severity = Column(Enum(ThreatSeverity), default=ThreatSeverity.MEDIUM)
    confidence = Column(Float, default=0.0)
    description = Column(Text)
    first_seen = Column(DateTime, default=func.now())
    last_seen = Column(DateTime, default=func.now())
    source = Column(String(100))
    is_active = Column(Boolean, default=True)
    extra_metadata = Column(JSON)  # Changed from 'metadata' to 'extra_metadata'
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    alerts = relationship("Alert", back_populates="indicator")

class Alert(Base):
    """Alert model."""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(Enum(ThreatSeverity), nullable=False)
    status = Column(Enum(AlertStatus), default=AlertStatus.PENDING)
    indicator_id = Column(Integer, ForeignKey("threat_indicators.id"))
    created_at = Column(DateTime, default=func.now())
    sent_at = Column(DateTime, nullable=True)
    extra_metadata = Column(JSON)  # Changed from 'metadata' to 'extra_metadata'
    
    # Relationships
    indicator = relationship("ThreatIndicator", back_populates="alerts")

class AlertConfiguration(Base):
    """Alert configuration model."""
    __tablename__ = "alert_configurations"
    
    id = Column(Integer, primary_key=True, index=True)
    config_name = Column(String(100), nullable=False, unique=True)
    email_enabled = Column(Boolean, default=True)
    email_recipients = Column(JSON)  # List of email addresses
    severity_threshold = Column(Enum(ThreatSeverity), default=ThreatSeverity.MEDIUM)
    max_alerts_per_hour = Column(Integer, default=10)
    smtp_server = Column(String(200))
    smtp_port = Column(Integer, default=587)
    smtp_username = Column(String(100))
    smtp_password = Column(String(200))  # Should be encrypted
    smtp_use_tls = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class SystemMetric(Base):
    """System metrics model."""
    __tablename__ = "system_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20))
    timestamp = Column(DateTime, default=func.now(), index=True)
    extra_metadata = Column(JSON)  # Changed from 'metadata' to 'extra_metadata'

class Feed(Base):
    """Threat feed model."""
    __tablename__ = "feeds"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    url = Column(String(500))
    feed_type = Column(String(50))
    is_active = Column(Boolean, default=True)
    last_updated = Column(DateTime)
    update_frequency = Column(Integer, default=60)  # minutes
    api_key = Column(String(200))
    extra_metadata = Column(JSON)  # Changed from 'metadata' to 'extra_metadata'
    created_at = Column(DateTime, default=func.now())

class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class APIKey(Base):
    """API Key model."""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    key_hash = Column(String(200), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    permissions = Column(JSON)  # List of permissions
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    last_used = Column(DateTime, nullable=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

class AuditLog(Base):
    """Audit log model."""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(100))
    ip_address = Column(String(45))
    user_agent = Column(Text)
    timestamp = Column(DateTime, default=func.now(), index=True)
    details = Column(JSON)
