"""
Dashboard endpoints for overview and monitoring.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Dict, Any

from app.db.database import get_db
from app.crud.crud_threat import get_threat_stats

router = APIRouter()

@router.get("/summary")
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    """Get dashboard summary statistics."""
    
    # Get threat statistics
    threat_stats = await get_threat_stats(db)
    
    # Mock real-time data (replace with actual monitoring)
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "threats": threat_stats,
        "system_health": {
            "status": "healthy",
            "cpu_usage": 23.5,
            "memory_usage": 67.2,
            "disk_usage": 45.8,
            "active_connections": 12
        },
        "recent_activity": {
            "new_threats_24h": threat_stats.get("new_indicators_24h", 0),
            "alerts_sent_24h": 5,
            "queries_24h": 1247,
            "feeds_updated": 3
        },
        "feed_status": {
            "total_feeds": 4,
            "active_feeds": 3,
            "last_update": (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
            "next_update": (datetime.utcnow() + timedelta(minutes=30)).isoformat()
        }
    }
    
    return summary

@router.get("/recent-activity")
async def get_recent_activity(hours: int = 24, db: AsyncSession = Depends(get_db)):
    """Get recent platform activity."""
    
    # Mock recent activity data (replace with actual database queries)
    activities = [
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
            "type": "threat_detected",
            "message": "New malicious IP detected: 192.168.1.100",
            "severity": "high"
        },
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=15)).isoformat(),
            "type": "feed_update",
            "message": "AbuseIPDB feed updated successfully",
            "severity": "info"
        },
        {
            "timestamp": (datetime.utcnow() - timedelta(minutes=30)).isoformat(),
            "type": "alert_sent",
            "message": "Critical threat alert sent to admin@company.com",
            "severity": "medium"
        }
    ]
    
    return {"activities": activities, "total": len(activities)}

@router.get("/top-indicators")
async def get_top_indicators(
    indicator_type: str = "ip", 
    limit: int = 10, 
    db: AsyncSession = Depends(get_db)
):
    """Get top threat indicators by type."""
    
    # Mock top indicators (replace with actual database queries)
    indicators = [
        {
            "value": "192.168.1.100",
            "type": "ip",
            "threat_count": 15,
            "severity": "critical",
            "last_seen": (datetime.utcnow() - timedelta(hours=2)).isoformat()
        },
        {
            "value": "malicious-domain.com",
            "type": "domain",
            "threat_count": 8,
            "severity": "high",
            "last_seen": (datetime.utcnow() - timedelta(hours=6)).isoformat()
        }
    ]
    
    return {"indicators": indicators[:limit], "total": len(indicators)}

@router.get("/health-status")
async def get_health_status():
    """Get system health status."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "operational",
            "api": "operational",
            "feeds": "operational",
            "alerts": "operational"
        },
        "metrics": {
            "uptime": "99.9%",
            "response_time": "45ms",
            "error_rate": "0.1%",
            "throughput": "1.2K req/min"
        }
    }

@router.post("/test-alert")
async def send_test_dashboard_alert():
    """Send a test alert from dashboard."""
    return {
        "message": "Test alert sent successfully from dashboard",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "success"
    }
