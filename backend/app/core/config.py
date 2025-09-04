"""
Configuration management for RTIP Platform.
Handles environment variables and application settings.
"""

from pydantic_settings import BaseSettings
from typing import List, Any, Dict
import os

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "RTIP Platform"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    API_KEY: str = "dev-api-key"
    
    # Database
    DATABASE_URL: str = "sqlite:///./rtip.db"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Email Configuration
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    ALERT_FROM_EMAIL: str = "alerts@rtip-platform.org"
    ALERT_TO_EMAIL: str = "admin@company.com"
    
    # External API Keys
    ABUSEIPDB_API_KEY: str = ""
    VIRUSTOTAL_API_KEY: str = ""
    
    # Feed Configuration
    FEED_UPDATE_INTERVAL: int = 60  # minutes
    CORRELATION_CHECK_INTERVAL: int = 15  # minutes
    
    # Alert Thresholds
    MIN_CONFIDENCE_SCORE: int = 70
    CRITICAL_ALERT_THRESHOLD: int = 3
    HIGH_ALERT_THRESHOLD: int = 2
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # SIEM Integration Settings
    SIEM_SPLUNK_ENABLED: bool = False
    SIEM_SPLUNK_URL: str = ""
    SIEM_SPLUNK_USERNAME: str = ""
    SIEM_SPLUNK_PASSWORD: str = ""
    SIEM_SPLUNK_HEC_TOKEN: str = ""
    SIEM_SPLUNK_INDEX: str = "threat_intel"

    SIEM_ELASTICSEARCH_ENABLED: bool = False
    SIEM_ELASTICSEARCH_URL: str = ""
    SIEM_ELASTICSEARCH_USERNAME: str = ""
    SIEM_ELASTICSEARCH_PASSWORD: str = ""
    SIEM_ELASTICSEARCH_INDEX: str = "threat-intel"

    SIEM_SENTINEL_ENABLED: bool = False
    SIEM_SENTINEL_URL: str = ""
    SIEM_SENTINEL_TENANT_ID: str = ""
    SIEM_SENTINEL_CLIENT_ID: str = ""
    SIEM_SENTINEL_CLIENT_SECRET: str = ""
    SIEM_SENTINEL_WORKSPACE_ID: str = ""

    SIEM_GENERIC_ENABLED: bool = False
    SIEM_GENERIC_WEBHOOK_URL: str = ""
    SIEM_GENERIC_API_KEY: str = ""
    SIEM_GENERIC_HEADERS: dict = {}

    SIEM_CONFIGS: Dict[str, Dict[str, Any]] = {
        "splunk": {
            "base_url": os.getenv("SPLUNK_URL", "https://localhost:8089"),
            "username": os.getenv("SPLUNK_USERNAME", ""),
            "password": os.getenv("SPLUNK_PASSWORD", ""),
            "token": os.getenv("SPLUNK_TOKEN", ""),
            "index": os.getenv("SPLUNK_INDEX", "rtip_threats")
        },
        "elasticsearch": {
            "hosts": os.getenv("ELASTICSEARCH_HOSTS", "localhost:9200").split(","),
            "username": os.getenv("ELASTICSEARCH_USERNAME", ""),
            "password": os.getenv("ELASTICSEARCH_PASSWORD", ""),
            "api_key": os.getenv("ELASTICSEARCH_API_KEY", ""),
            "index_prefix": os.getenv("ELASTICSEARCH_INDEX_PREFIX", "rtip")
        }
    }
    
    # Grafana Integration Settings
    GRAFANA_URL: str = os.getenv("GRAFANA_URL", "http://localhost:3000")
    GRAFANA_API_TOKEN: str = os.getenv("GRAFANA_API_TOKEN", "")
    GRAFANA_USERNAME: str = "admin"
    GRAFANA_PASSWORD: str = "admin"
    
    # Threat Hunting Settings
    THREAT_HUNTING_MAX_RESULTS: int = int(os.getenv("THREAT_HUNTING_MAX_RESULTS", "5000"))
    THREAT_HUNTING_DEFAULT_LIMIT: int = int(os.getenv("THREAT_HUNTING_DEFAULT_LIMIT", "1000"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env file

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)

# Global settings instance
settings = Settings()
