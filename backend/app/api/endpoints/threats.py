"""
Threat intelligence endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.db.database import get_db
from app.db.models import ThreatIndicator, ThreatSeverity, IndicatorType
from app.schemas.threat import ThreatIndicatorResponse, ThreatIndicatorCreate, ThreatIndicatorUpdate
from app.crud.crud_threat import (
    get_threat_indicator as get_threat, 
    get_threats, 
    create_threat_indicator as create_threat, 
    update_threat_indicator as update_threat, 
    delete_threat_indicator as delete_threat,
    search_threats, 
    get_threat_stats
)

router = APIRouter()

@router.get("/", response_model=List[ThreatIndicatorResponse])
async def read_threats(
    skip: int = 0,
    limit: int = 100,
    severity: Optional[ThreatSeverity] = None,
    indicator_type: Optional[IndicatorType] = None,
    is_active: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Get a list of threat indicators."""
    threats = await get_threats(
        db, skip=skip, limit=limit, 
        severity=severity, indicator_type=indicator_type, is_active=is_active
    )
    return threats

@router.get("/search/")
async def search_threat_indicators(
    q: str = Query(..., description="Search query"),
    limit: int = Query(50, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Search threat indicators."""
    results = await search_threats(db, query=q, limit=limit)
    return {"results": results, "total": len(results)}

@router.get("/stats/")
async def get_threat_statistics(db: AsyncSession = Depends(get_db)):
    """Get threat intelligence statistics."""
    stats = await get_threat_stats(db)
    return stats

@router.get("/check")
async def check_indicators(
    indicators: List[str] = Query(..., description="List of indicators to check"),
    db: AsyncSession = Depends(get_db)
):
    """Check multiple indicators against threat intelligence."""
    results = []
    for indicator in indicators:
        # Simple search by value
        threats = await search_threats(db, query=indicator, limit=10)
        results.append({
            "indicator": indicator,
            "is_threat": len(threats) > 0,
            "matches": threats[:5],  # Return top 5 matches
            "threat_count": len(threats)
        })
    return {"results": results}

@router.get("/critical/")
async def get_critical_threats(
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get critical threats."""
    threats = await get_threats(
        db, limit=limit, severity=ThreatSeverity.CRITICAL, is_active=True
    )
    return threats

@router.post("/analyze/{indicator}")
async def analyze_indicator(
    indicator: str,
    indicator_type: IndicatorType = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Analyze a single indicator."""
    # Check if indicator exists in database
    existing_threats = await search_threats(db, query=indicator, limit=10)
    
    analysis = {
        "indicator": indicator,
        "type": indicator_type.value,
        "timestamp": datetime.utcnow().isoformat(),
        "database_matches": len(existing_threats),
        "threats_found": existing_threats,
        "risk_score": min(len(existing_threats) * 20, 100),  # Simple scoring
        "recommendations": []
    }
    
    # Add basic recommendations
    if len(existing_threats) > 0:
        analysis["recommendations"].append("Block this indicator")
        analysis["recommendations"].append("Monitor related traffic")
    else:
        analysis["recommendations"].append("Continue monitoring")
    
    return analysis

@router.get("/{threat_id}", response_model=ThreatIndicatorResponse)
async def read_threat(threat_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific threat by ID."""
    threat = await get_threat(db, threat_id=threat_id)
    if threat is None:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat

@router.post("/", response_model=ThreatIndicatorResponse)
async def create_threat_indicator(
    threat: ThreatIndicatorCreate, 
    db: AsyncSession = Depends(get_db)
):
    """Create a new threat indicator."""
    return await create_threat(db=db, threat=threat)

@router.put("/{threat_id}", response_model=ThreatIndicatorResponse)
async def update_threat_indicator(
    threat_id: int,
    threat_update: ThreatIndicatorUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a threat indicator."""
    threat = await update_threat(db, threat_id=threat_id, threat=threat_update)
    if threat is None:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat

@router.delete("/{threat_id}")
async def delete_threat_indicator(threat_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a threat indicator."""
    success = await delete_threat(db, threat_id=threat_id)
    if not success:
        raise HTTPException(status_code=404, detail="Threat not found")
    return {"message": "Threat indicator deleted successfully"}
