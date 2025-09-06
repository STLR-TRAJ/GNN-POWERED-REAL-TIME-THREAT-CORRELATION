"""
API v1 router configuration.
"""

from fastapi import APIRouter

# Import endpoint routers
from app.api.endpoints import threats, alerts, dashboard, system

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    threats.router,
    prefix="/threats",
    tags=["threats"]
)

api_router.include_router(
    alerts.router,
    prefix="/alerts",
    tags=["alerts"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["dashboard"]
)

api_router.include_router(
    system.router,
    prefix="/system",
    tags=["system"]
)
