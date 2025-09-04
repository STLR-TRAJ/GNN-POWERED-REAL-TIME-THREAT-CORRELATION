"""
Enhanced Pydantic schemas for threat-related API requests and responses.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ThreatType(str, Enum):
    """Enumeration of supported threat indicator types."""
    IP = "ip"
    DOMAIN = "domain"
    URL = "url"
    FILE_HASH = "file_hash"
    EMAIL = "email"

class SeverityLevel(str, Enum):
    """Enumeration of threat severity levels."""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class ThreatIndicatorBase(BaseModel):
    """Base schema for threat indicators with enhanced fields."""
    value: str = Field(..., description="The threat indicator value")
    type: ThreatType = Field(..., description="Type of threat indicator")
    source: str = Field(..., description="Source of the threat intelligence")
    severity: SeverityLevel = Field(..., description="Severity level of the threat")
    confidence: int = Field(default=0, ge=0, le=100, description="Confidence score (0-100)")
    tags: List[str] = Field(default_factory=list, description="Associated tags")
    description: Optional[str] = Field(None, description="Additional context")
    references: List[str] = Field(default_factory=list, description="Reference URLs")
    
    # Enhanced fields
    reported_by: Optional[str] = Field(None, description="Entity or individual reporting the threat")
    related_cves: List[str] = Field(default_factory=list, description="Array of related CVE IDs")
    malware_family: Optional[str] = Field(None, description="Identified malware family")
    threat_score: int = Field(default=0, ge=0, le=100, description="Calculated threat score (0-100)")

class ThreatIndicatorCreate(ThreatIndicatorBase):
    """Schema for creating a new threat indicator."""
    pass

class ThreatIndicatorUpdate(BaseModel):
    """Schema for updating an existing threat indicator."""
    severity: Optional[SeverityLevel] = None
    confidence: Optional[int] = Field(None, ge=0, le=100)
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    references: Optional[List[str]] = None
    is_active: Optional[bool] = None
    reported_by: Optional[str] = None
    related_cves: Optional[List[str]] = None
    malware_family: Optional[str] = None
    threat_score: Optional[int] = Field(None, ge=0, le=100)

class ThreatIndicatorResponse(ThreatIndicatorBase):
    """Schema for threat indicator API responses."""
    id: int
    first_seen: datetime
    last_seen: datetime
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ThreatSearchRequest(BaseModel):
    """Schema for threat search requests."""
    query: str = Field(..., min_length=1, description="Search query (IP, domain, URL, etc.)")
    type: Optional[ThreatType] = Field(None, description="Filter by threat type")
    severity: Optional[SeverityLevel] = Field(None, description="Filter by severity")
    source: Optional[str] = Field(None, description="Filter by source")
    malware_family: Optional[str] = Field(None, description="Filter by malware family")
    min_threat_score: Optional[int] = Field(None, ge=0, le=100, description="Minimum threat score")
    limit: int = Field(default=50, ge=1, le=1000, description="Maximum results to return")

class ThreatSearchResponse(BaseModel):
    """Schema for threat search results."""
    query: str
    total_results: int
    results: List[ThreatIndicatorResponse]
    execution_time_ms: float

class ThreatCheckRequest(BaseModel):
    """Schema for checking if an indicator is malicious."""
    indicators: List[str] = Field(..., min_items=1, max_items=100, description="List of indicators to check")

class ThreatCheckResult(BaseModel):
    """Schema for individual threat check result."""
    indicator: str
    is_malicious: bool
    severity: Optional[SeverityLevel] = None
    confidence: int = 0
    sources: List[str] = Field(default_factory=list)
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    reported_by: Optional[str] = None
    related_cves: List[str] = Field(default_factory=list)
    malware_family: Optional[str] = None
    threat_score: int = 0

class ThreatCheckResponse(BaseModel):
    """Schema for bulk threat check response."""
    results: List[ThreatCheckResult]
    total_checked: int
    malicious_count: int
    execution_time_ms: float

class ThreatStatsResponse(BaseModel):
    """Schema for threat statistics."""
    total_threats: int
    active_threats: int
    threats_by_severity: Dict[str, int]
    threats_by_type: Dict[str, int]
    threats_by_source: Dict[str, int]
    threats_by_malware_family: Dict[str, int]
    average_threat_score: float
    recent_threats_24h: int
    last_updated: datetime
