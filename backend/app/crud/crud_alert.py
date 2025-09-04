"""
CRUD operations for alert configurations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.db.models import AlertConfiguration
from app.schemas.alert import AlertConfigurationRequest

async def create_alert_configuration(
    db: AsyncSession,
    config_data: AlertConfigurationRequest
) -> AlertConfiguration:
    """Create a new alert configuration."""
    db_config = AlertConfiguration(**config_data.model_dump())
    db.add(db_config)
    await db.commit()
    await db.refresh(db_config)
    return db_config

async def get_alert_configuration(
    db: AsyncSession,
    config_id: int
) -> Optional[AlertConfiguration]:
    """Get an alert configuration by ID."""
    result = await db.execute(
        select(AlertConfiguration).where(AlertConfiguration.id == config_id)
    )
    return result.scalar_one_or_none()

async def get_alert_configuration_by_name(
    db: AsyncSession,
    config_name: str
) -> Optional[AlertConfiguration]:
    """Get an alert configuration by name."""
    result = await db.execute(
        select(AlertConfiguration).where(AlertConfiguration.config_name == config_name)
    )
    return result.scalar_one_or_none()

async def get_alert_configurations(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True
) -> List[AlertConfiguration]:
    """Get a list of alert configurations."""
    query = select(AlertConfiguration)
    
    if active_only:
        query = query.where(AlertConfiguration.is_active == True)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def update_alert_configuration(
    db: AsyncSession,
    config_id: int,
    config_data: Dict[str, Any]
) -> Optional[AlertConfiguration]:
    """Update an alert configuration."""
    db_config = await get_alert_configuration(db, config_id)
    if not db_config:
        return None
    
    for field, value in config_data.items():
        if hasattr(db_config, field):
            setattr(db_config, field, value)
    
    db_config.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(db_config)
    return db_config

async def delete_alert_configuration(
    db: AsyncSession,
    config_id: int
) -> bool:
    """Delete an alert configuration."""
    result = await db.execute(
        delete(AlertConfiguration).where(AlertConfiguration.id == config_id)
    )
    await db.commit()
    return result.rowcount > 0

async def get_default_alert_configuration(db: AsyncSession) -> Optional[AlertConfiguration]:
    """Get or create the default alert configuration."""
    config = await get_alert_configuration_by_name(db, "default")
    
    if not config:
        # Create default configuration
        from app.core.config import settings
        default_config = AlertConfiguration(
            config_name="default",
            email_enabled=True,
            email_recipients=[settings.ALERT_TO_EMAIL] if settings.ALERT_TO_EMAIL else [],
            severity_threshold="High",
            max_alerts_per_hour=10,
            smtp_server=settings.SMTP_SERVER,
            smtp_port=settings.SMTP_PORT,
            smtp_username=settings.SMTP_USERNAME,
            smtp_password=settings.SMTP_PASSWORD,
            smtp_use_tls=True,
            is_active=True
        )
        
        db.add(default_config)
        await db.commit()
        await db.refresh(default_config)
        config = default_config
    
    return config
