"""
CRUD operations for threat indicators.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from app.db.models import ThreatIndicator, FeedStatus
from app.schemas.threat import ThreatIndicatorCreate, ThreatIndicatorUpdate, ThreatType, SeverityLevel

async def create_threat_indicator(
    db: AsyncSession,
    threat_data: ThreatIndicatorCreate
) -> ThreatIndicator:
    """Create a new threat indicator."""
    db_threat = ThreatIndicator(**threat_data.model_dump())
    db.add(db_threat)
    await db.commit()
    await db.refresh(db_threat)
    return db_threat

async def get_threat_indicator(
    db: AsyncSession,
    threat_id: int
) -> Optional[ThreatIndicator]:
    """Get a threat indicator by ID."""
    result = await db.execute(
        select(ThreatIndicator).where(ThreatIndicator.id == threat_id)
    )
    return result.scalar_one_or_none()

async def get_threat_by_value(
    db: AsyncSession,
    value: str,
    type: Optional[str] = None
) -> Optional[ThreatIndicator]:
    """Get a threat indicator by its value and optionally type."""
    query = select(ThreatIndicator).where(ThreatIndicator.value == value)
    if type:
        query = query.where(ThreatIndicator.type == type)
    
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def get_threats(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None,
    type: Optional[str] = None,
    source: Optional[str] = None,
    active_only: bool = True
) -> List[ThreatIndicator]:
    """Get a list of threat indicators with optional filtering."""
    query = select(ThreatIndicator)
    
    # Apply filters
    conditions = []
    if active_only:
        conditions.append(ThreatIndicator.is_active == True)
    if severity:
        conditions.append(ThreatIndicator.severity == severity)
    if type:
        conditions.append(ThreatIndicator.type == type)
    if source:
        conditions.append(ThreatIndicator.source == source)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Order by last_seen descending
    query = query.order_by(desc(ThreatIndicator.last_seen))
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

async def search_threats(
    db: AsyncSession,
    search_query: str,
    limit: int = 50
) -> List[ThreatIndicator]:
    """Search threat indicators by value."""
    # Simple search - in production, consider full-text search
    query = select(ThreatIndicator).where(
        or_(
            ThreatIndicator.value.ilike(f"%{search_query}%"),
            ThreatIndicator.description.ilike(f"%{search_query}%")
        )
    ).order_by(desc(ThreatIndicator.last_seen)).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

async def update_threat_indicator(
    db: AsyncSession,
    threat_id: int,
    threat_update: ThreatIndicatorUpdate
) -> Optional[ThreatIndicator]:
    """Update a threat indicator."""
    db_threat = await get_threat_indicator(db, threat_id)
    if not db_threat:
        return None
    
    update_data = threat_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_threat, field, value)
    
    db_threat.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_threat)
    return db_threat

async def upsert_threat_indicator(
    db: AsyncSession,
    threat_data: ThreatIndicatorCreate
) -> ThreatIndicator:
    """Create or update a threat indicator (upsert operation)."""
    existing = await get_threat_by_value(db, threat_data.value, threat_data.type)
    
    if existing:
        # Update existing record
        existing.last_seen = datetime.utcnow()
        existing.confidence = max(existing.confidence, threat_data.confidence)
        
        # Merge tags
        existing_tags = set(existing.tags or [])
        new_tags = set(threat_data.tags or [])
        existing.tags = list(existing_tags.union(new_tags))
        
        # Update severity if new one is higher
        severity_order = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}
        if severity_order.get(threat_data.severity, 0) > severity_order.get(existing.severity, 0):
            existing.severity = threat_data.severity
        
        # Merge references
        existing_refs = set(existing.references or [])
        new_refs = set(threat_data.references or [])
        existing.references = list(existing_refs.union(new_refs))
        
        existing.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(existing)
        return existing
    else:
        # Create new record
        return await create_threat_indicator(db, threat_data)

async def get_threat_stats(db: AsyncSession) -> Dict[str, Any]:
    """Get threat statistics for dashboard."""
    # Total threats
    total_result = await db.execute(select(func.count(ThreatIndicator.id)))
    total_threats = total_result.scalar()
    
    # Active threats
    active_result = await db.execute(
        select(func.count(ThreatIndicator.id)).where(ThreatIndicator.is_active == True)
    )
    active_threats = active_result.scalar()
    
    # Recent threats (last 24 hours)
    recent_cutoff = datetime.utcnow() - timedelta(hours=24)
    recent_result = await db.execute(
        select(func.count(ThreatIndicator.id)).where(
            ThreatIndicator.created_at >= recent_cutoff
        )
    )
    recent_threats = recent_result.scalar()
    
    # Threats by severity
    severity_result = await db.execute(
        select(ThreatIndicator.severity, func.count(ThreatIndicator.id))
        .where(ThreatIndicator.is_active == True)
        .group_by(ThreatIndicator.severity)
    )
    threats_by_severity = {row[0]: row[1] for row in severity_result.fetchall()}
    
    # Threats by type
    type_result = await db.execute(
        select(ThreatIndicator.type, func.count(ThreatIndicator.id))
        .where(ThreatIndicator.is_active == True)
        .group_by(ThreatIndicator.type)
    )
    threats_by_type = {row[0]: row[1] for row in type_result.fetchall()}
    
    # Threats by source
    source_result = await db.execute(
        select(ThreatIndicator.source, func.count(ThreatIndicator.id))
        .where(ThreatIndicator.is_active == True)
        .group_by(ThreatIndicator.source)
    )
    threats_by_source = {row[0]: row[1] for row in source_result.fetchall()}
    
    return {
        "total_threats": total_threats,
        "active_threats": active_threats,
        "recent_threats_24h": recent_threats,
        "threats_by_severity": threats_by_severity,
        "threats_by_type": threats_by_type,
        "threats_by_source": threats_by_source,
        "last_updated": datetime.utcnow()
    }

async def get_critical_threats(
    db: AsyncSession,
    limit: int = 10
) -> List[ThreatIndicator]:
    """Get the most critical active threats."""
    query = select(ThreatIndicator).where(
        and_(
            ThreatIndicator.is_active == True,
            ThreatIndicator.severity.in_(["Critical", "High"])
        )
    ).order_by(
        desc(ThreatIndicator.severity),
        desc(ThreatIndicator.confidence),
        desc(ThreatIndicator.last_seen)
    ).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

async def check_indicators_bulk(
    db: AsyncSession,
    indicators: List[str]
) -> Dict[str, Optional[ThreatIndicator]]:
    """Check multiple indicators for threats in bulk."""
    query = select(ThreatIndicator).where(
        and_(
            ThreatIndicator.value.in_(indicators),
            ThreatIndicator.is_active == True
        )
    )
    
    result = await db.execute(query)
    threats = result.scalars().all()
    
    # Create a mapping of indicator -> threat
    threat_map = {threat.value: threat for threat in threats}
    
    # Return results for all requested indicators
    return {indicator: threat_map.get(indicator) for indicator in indicators}
