"""
Enhanced Pydantic schemas for alert-related API requests and responses.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AlertType(str, Enum):
    """Enumeration of alert types."""
    EMAIL = "email"
    WEBHOOK = "webhook"
    SMS = "sms"

class AlertStatus(str, Enum):
    """Enumeration of alert statuses."""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    CANCELLED = "cancelled"

class AlertSeverity(str, Enum):
    """Enumeration of alert severity levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class AlertBase(BaseModel):
    """Base schema for alerts."""
    alert_type: AlertType = Field(..., description="Type of alert")
    severity: AlertSeverity = Field(..., description="Alert severity level")
    subject: str = Field(..., min_length=1, max_length=255, description="Alert subject")
    message: str = Field(..., min_length=1, description="Alert message content")
    recipient: str = Field(..., description="Alert recipient (email, phone, webhook URL)")

class AlertCreate(AlertBase):
    """Schema for creating a new alert."""
    threat_indicators: List[int] = Field(default_factory=list, description="Related threat indicator IDs")

class AlertResponse(AlertBase):
    """Schema for alert API responses."""
    id: int
    status: AlertStatus
    error_message: Optional[str] = None
    threat_indicators: List[int]
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class AlertConfigurationRequest(BaseModel):
    """Schema for configuring alert settings."""
    config_name: str = Field(..., description="Configuration name")
    email_enabled: bool = Field(default=True, description="Enable email alerts")
    email_recipients: List[EmailStr] = Field(default_factory=list, description="Email recipients")
    severity_threshold: AlertSeverity = Field(default=AlertSeverity.HIGH, description="Minimum severity for alerts")
    max_alerts_per_hour: int = Field(default=10, ge=1, le=100, description="Maximum alerts per hour")
    alert_template: Optional[str] = Field(None, description="Custom alert template")
    smtp_server: Optional[str] = Field(None, description="SMTP server address")
    smtp_port: int = Field(default=587, description="SMTP server port")
    smtp_username: Optional[str] = Field(None, description="SMTP username")
    smtp_password: Optional[str] = Field(None, description="SMTP password")
    smtp_use_tls: bool = Field(default=True, description="Use TLS for SMTP")

class AlertConfigurationResponse(BaseModel):
    """Schema for alert configuration responses."""
    id: int
    config_name: str
    email_enabled: bool
    email_recipients: List[str]
    severity_threshold: str
    max_alerts_per_hour: int
    smtp_server: Optional[str] = None
    smtp_port: int
    smtp_username: Optional[str] = None
    smtp_use_tls: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AlertStatsResponse(BaseModel):
    """Schema for alert statistics."""
    total_alerts: int
    alerts_sent: int
    alerts_failed: int
    alerts_by_severity: Dict[str, int]
    alerts_by_type: Dict[str, int]
    recent_alerts_24h: int
    last_alert_sent: Optional[datetime] = None

class ThreatAlertData(BaseModel):
    """Schema for threat data included in alerts."""
    indicator: str
    type: str
    severity: str
    confidence: int
    source: str
    first_seen: datetime
    description: Optional[str] = None
    recommended_action: str
    reported_by: Optional[str] = None
    related_cves: List[str] = Field(default_factory=list)
    malware_family: Optional[str] = None
    threat_score: int = 0

class AlertTemplate(BaseModel):
    """Schema for alert email templates."""
    subject_template: str = Field(..., description="Email subject template")
    body_template: str = Field(..., description="Email body template")
    include_threat_details: bool = Field(default=True, description="Include detailed threat information")
    include_mitigation_steps: bool = Field(default=True, description="Include recommended mitigation steps")
    include_related_cves: bool = Field(default=True, description="Include related CVE information")
    include_malware_family: bool = Field(default=True, description="Include malware family information")
