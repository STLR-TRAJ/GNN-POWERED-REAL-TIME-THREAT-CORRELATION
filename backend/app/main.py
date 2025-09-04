"""
Real-time Threat Intelligence Platform (RTIP) - Main Application
FastAPI application entry point with comprehensive threat intelligence capabilities.
"""

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import settings
from app.core.security import verify_api_key
from app.db.database import engine, create_tables
from app.api.api_v1 import api_router
from app.services.feed_ingestor import FeedIngestor
from app.services.correlation_engine import CorrelationEngine
from app.services.monitoring import SystemMonitor
from app.services.training_service import TrainingService

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info("🚀 Starting RTIP Platform...")
    
    # Create database tables
    await create_tables()
    logger.info("✅ Database tables created/verified")
    
    # Initialize services
    feed_ingestor = FeedIngestor()
    correlation_engine = CorrelationEngine()
    system_monitor = SystemMonitor()
    training_service = TrainingService()
    
    # Initialize training modules
    await training_service.initialize_default_modules()
    logger.info("✅ Training modules initialized")
    
    # Schedule background tasks
    scheduler.add_job(
        feed_ingestor.run_ingestion_cycle,
        IntervalTrigger(minutes=settings.FEED_UPDATE_INTERVAL),
        id="feed_ingestion",
        name="Threat Feed Ingestion",
        replace_existing=True
    )
    
    scheduler.add_job(
        correlation_engine.run_correlation_cycle,
        IntervalTrigger(minutes=settings.CORRELATION_CHECK_INTERVAL),
        id="correlation_check",
        name="Threat Correlation Check",
        replace_existing=True
    )
    
    # Add system monitoring job
    scheduler.add_job(
        system_monitor.run_monitoring_cycle,
        IntervalTrigger(minutes=5),  # Monitor every 5 minutes
        id="system_monitoring",
        name="System Performance Monitoring",
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("⏰ Background tasks scheduled")
    
    # Run initial tasks
    try:
        await feed_ingestor.run_ingestion_cycle()
        logger.info("✅ Initial threat feed ingestion completed")
    except Exception as e:
        logger.error(f"❌ Initial ingestion failed: {e}")
    
    # Run initial monitoring
    try:
        await system_monitor.run_monitoring_cycle()
        logger.info("✅ Initial system monitoring completed")
    except Exception as e:
        logger.error(f"❌ Initial monitoring failed: {e}")
    
    logger.info("🎯 RTIP Platform started successfully!")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down RTIP Platform...")
    scheduler.shutdown()
    logger.info("✅ RTIP Platform shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="Real-time Threat Intelligence Platform (RTIP)",
    description="""
    A lightweight, open-source threat intelligence platform designed for SMEs.
    
    ## Features
    * **Automated Threat Feed Ingestion** - AbuseIPDB, CISA, CVE feeds
    * **Real-time Correlation** - Smart threat pattern detection
    * **System Monitoring** - Performance tracking and health alerts
    * **Webhook Integration** - External system notifications
    * **User Training** - Interactive cybersecurity education
    * **Actionable Alerts** - Clear, non-technical notifications
    
    ## Authentication
    All endpoints require an API key in the Authorization header:
    `Authorization: Bearer YOUR_API_KEY`
    """,
    version="1.0.0",
    contact={
        "name": "RTIP Support",
        "email": "support@rtip-platform.org",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security scheme
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key authentication."""
    if not verify_api_key(credentials.credentials):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"api_key": credentials.credentials}

# Include API routes
app.include_router(
    api_router,
    prefix="/api/v1",
    dependencies=[Depends(get_current_user)]
)

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with platform information."""
    return {
        "message": "Real-time Threat Intelligence Platform (RTIP)",
        "version": "1.0.0",
        "description": "Democratizing cybersecurity intelligence for SMEs",
        "features": [
            "Threat Intelligence",
            "System Monitoring", 
            "Webhook Integration",
            "User Training",
            "Real-time Alerts"
        ],
        "docs": "/docs",
        "health": "/health",
        "api": "/api/v1"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Enhanced health check endpoint with system monitoring."""
    try:
        system_monitor = SystemMonitor()
        health_summary = await system_monitor.get_system_health_summary()
        
        return {
            "status": "healthy" if health_summary["overall_health"] in ["excellent", "good"] else "degraded",
            "timestamp": "2025-01-20T15:48:55Z",
            "services": {
                "api": "operational",
                "database": "operational",
                "scheduler": "operational" if scheduler.running else "stopped",
                "feeds": "operational",
                "monitoring": "operational",
                "training": "operational"
            },
            "system_health": health_summary,
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/metrics", tags=["Monitoring"])
async def get_metrics(current_user: dict = Depends(get_current_user)):
    """Get platform metrics for monitoring."""
    from app.crud.crud_threat import get_threat_stats
    from app.db.database import get_db
    
    system_monitor = SystemMonitor()
    
    async with get_db() as db:
        threat_stats = await get_threat_stats(db)
    
    system_health = await system_monitor.get_system_health_summary()
    
    return {
        "threats": threat_stats,
        "system": system_health,
        "scheduler": {
            "running": scheduler.running,
            "jobs": len(scheduler.get_jobs())
        },
        "uptime": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
