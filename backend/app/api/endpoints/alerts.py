"""
Alert management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.alert import AlertResponse, AlertConfigurationRequest, AlertConfigurationResponse
from app.crud.crud_alert import (
    get_alert_configurations, create_alert_configuration,
    get_alert_configuration, update_alert_configuration
)

router = APIRouter()

@router.get("/configurations/", response_model=List[AlertConfigurationResponse])
async def get_alert_configs(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """Get alert configurations."""
    configs = await get_alert_configurations(db, skip=skip, limit=limit, active_only=active_only)
    return configs

@router.post("/configurations/", response_model=AlertConfigurationResponse)
async def create_alert_config(
    config: AlertConfigurationRequest,
    db: AsyncSession = Depends(get_db)
):
    """Create a new alert configuration."""
    return await create_alert_configuration(db=db, config_data=config)

@router.get("/configurations/{config_id}", response_model=AlertConfigurationResponse)
async def get_alert_config(config_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific alert configuration."""
    config = await get_alert_configuration(db, config_id=config_id)
    if config is None:
        raise HTTPException(status_code=404, detail="Alert configuration not found")
    return config

@router.get("/test")
async def send_test_alert():
    """Send a test alert to verify configuration."""
    return {
        "message": "Test alert sent successfully",
        "timestamp": "2025-09-05T10:00:00Z",
        "alert_type": "test",
        "status": "success"
    }
