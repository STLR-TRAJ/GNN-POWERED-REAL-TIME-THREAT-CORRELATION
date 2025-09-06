"""
System management and monitoring endpoints.
"""

from fastapi import APIRouter
from datetime import datetime
import psutil
import platform
import sys

router = APIRouter()

@router.get("/info")
async def get_system_info():
    """Get system information."""
    return {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        },
        "python": {
            "version": sys.version,
            "executable": sys.executable
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/health")
async def system_health():
    """Get detailed system health metrics."""
    
    try:
        # CPU information
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory information
        memory = psutil.virtual_memory()
        
        # Disk information
        disk = psutil.disk_usage('/')
        
        # Network information (if available)
        try:
            network = psutil.net_io_counters()
            network_stats = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
        except:
            network_stats = {"error": "Network stats unavailable"}
        
        health_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "healthy",
            "cpu": {
                "usage_percent": cpu_percent,
                "count": cpu_count
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "usage_percent": memory.percent
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "usage_percent": (disk.used / disk.total) * 100
            },
            "network": network_stats,
            "processes": len(psutil.pids())
        }
        
        return health_data
        
    except Exception as e:
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "status": "error",
            "error": str(e),
            "message": "Unable to collect system metrics"
        }

@router.get("/status")
async def get_system_status():
    """Get basic system status."""
    return {
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "environment": "development"
    }
