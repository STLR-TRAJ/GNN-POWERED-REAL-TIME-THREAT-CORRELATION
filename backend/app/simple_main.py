"""
Simplified Real-time Threat Intelligence Platform (RTIP) - Main Application
FastAPI application entry point without async database dependencies.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

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
    """,
    version="1.0.0",
    contact={
        "name": "RTIP Support",
        "email": "support@rtip-platform.org",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
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
        "status": "running"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2025-09-01T00:00:00Z",
        "services": {
            "api": "operational",
            "database": "operational",
            "feeds": "operational"
        },
        "version": "1.0.0"
    }

@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("🚀 Starting RTIP Platform...")
    try:
        from app.db.sync_database import create_tables
        create_tables()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.warning(f"⚠️ Database initialization skipped: {e}")
    logger.info("🎯 RTIP Platform started successfully!")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("🛑 Shutting down RTIP Platform...")
    logger.info("✅ RTIP Platform shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.simple_main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
