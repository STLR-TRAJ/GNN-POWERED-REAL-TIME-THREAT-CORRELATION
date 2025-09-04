"""
CRUD operations for CVE (Common Vulnerabilities and Exposures) data.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from app.db.models import CVEData
from app.schemas.threat import SeverityLevel

async def create_cve(
    db: AsyncSession,
    cve_id: str,
    description: str,
    cvss_score: Optional[float] = None,
    severity: Optional[str] = None,
    published_date: Optional[datetime] = None,
    references: Optional[List[str]] = None,
    affected_products: Optional[List[str]] = None,
    tags: Optional[List[str]] = None
) -> CVEData:
    """Create a new CVE record."""
    db_cve = CVEData(
        id=cve_id,
        description=description,
        cvss_score=cvss_score,
        severity=severity or _calculate_severity_from_cvss(cvss_score),
        published_date=published_date,
        references=references or [],
        affected_products=affected_products or [],
        tags=tags or []
    )
    
    db.add(db_cve)
    await db.commit()
    await db.refresh(db_cve)
    return db_cve

async def get_cve(db: AsyncSession, cve_id: str) -> Optional[CVEData]:
    """Get a CVE by its ID."""
    result = await db.execute(select(CVEData).where(CVEData.id == cve_id))
    return result.scalar_one_or_none()

async def get_cves(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    severity: Optional[str] = None,
    min_cvss_score: Optional[float] = None,
    active_only: bool = True
) -> List[CVEData]:
    """Get a list of CVEs with optional filtering."""
    query = select(CVEData)
    
    conditions = []
    if active_only:
        conditions.append(CVEData.is_active == True)
    if severity:
        conditions.append(CVEData.severity == severity)
    if min_cvss_score is not None:
        conditions.append(CVEData.cvss_score >= min_cvss_score)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.order_by(desc(CVEData.published_date)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

async def search_cves(
    db: AsyncSession,
    search_query: str,
    limit: int = 50
) -> List[CVEData]:
    """Search CVEs by ID or description."""
    query = select(CVEData).where(
        or_(
            CVEData.id.ilike(f"%{search_query}%"),
            CVEData.description.ilike(f"%{search_query}%")
        )
    ).order_by(desc(CVEData.published_date)).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

async def upsert_cve(
    db: AsyncSession,
    cve_id: str,
    description: str,
    cvss_score: Optional[float] = None,
    severity: Optional[str] = None,
    published_date: Optional[datetime] = None,
    modified_date: Optional[datetime] = None,
    references: Optional[List[str]] = None,
    affected_products: Optional[List[str]] = None,
    tags: Optional[List[str]] = None
) -> CVEData:
    """Create or update a CVE record."""
    existing = await get_cve(db, cve_id)
    
    if existing:
        # Update existing record
        existing.description = description
        existing.cvss_score = cvss_score
        existing.severity = severity or _calculate_severity_from_cvss(cvss_score)
        existing.modified_date = modified_date or datetime.utcnow()
        
        if references:
            existing_refs = set(existing.references or [])
            new_refs = set(references)
            existing.references = list(existing_refs.union(new_refs))
        
        if affected_products:
            existing_products = set(existing.affected_products or [])
            new_products = set(affected_products)
            existing.affected_products = list(existing_products.union(new_products))
        
        if tags:
            existing_tags = set(existing.tags or [])
            new_tags = set(tags)
            existing.tags = list(existing_tags.union(new_tags))
        
        existing.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(existing)
        return existing
    else:
        # Create new record
        return await create_cve(
            db=db,
            cve_id=cve_id,
            description=description,
            cvss_score=cvss_score,
            severity=severity,
            published_date=published_date,
            references=references,
            affected_products=affected_products,
            tags=tags
        )

async def get_critical_cves(
    db: AsyncSession,
    days: int = 30,
    limit: int = 20
) -> List[CVEData]:
    """Get critical CVEs from the last N days."""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    query = select(CVEData).where(
        and_(
            CVEData.is_active == True,
            CVEData.severity.in_(["Critical", "High"]),
            CVEData.published_date >= cutoff_date
        )
    ).order_by(
        desc(CVEData.cvss_score),
        desc(CVEData.published_date)
    ).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()

async def get_cve_stats(db: AsyncSession) -> Dict[str, Any]:
    """Get CVE statistics."""
    # Total CVEs
    total_result = await db.execute(select(func.count(CVEData.id)))
    total_cves = total_result.scalar()
    
    # Active CVEs
    active_result = await db.execute(
        select(func.count(CVEData.id)).where(CVEData.is_active == True)
    )
    active_cves = active_result.scalar()
    
    # Recent CVEs (last 30 days)
    recent_cutoff = datetime.utcnow() - timedelta(days=30)
    recent_result = await db.execute(
        select(func.count(CVEData.id)).where(
            CVEData.published_date >= recent_cutoff
        )
    )
    recent_cves = recent_result.scalar()
    
    # CVEs by severity
    severity_result = await db.execute(
        select(CVEData.severity, func.count(CVEData.id))
        .where(CVEData.is_active == True)
        .group_by(CVEData.severity)
    )
    cves_by_severity = {row[0]: row[1] for row in severity_result.fetchall()}
    
    return {
        "total_cves": total_cves,
        "active_cves": active_cves,
        "recent_cves_30d": recent_cves,
        "cves_by_severity": cves_by_severity,
        "last_updated": datetime.utcnow()
    }

def _calculate_severity_from_cvss(cvss_score: Optional[float]) -> str:
    """Calculate severity level from CVSS score."""
    if cvss_score is None:
        return "Medium"
    
    if cvss_score >= 9.0:
        return "Critical"
    elif cvss_score >= 7.0:
        return "High"
    elif cvss_score >= 4.0:
        return "Medium"
    else:
        return "Low"
