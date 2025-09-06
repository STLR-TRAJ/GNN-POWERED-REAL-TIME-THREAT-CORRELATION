"""
Feed ingestion service for threat intelligence feeds.
Integrates with cloud services for threat data distribution.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import httpx
import asyncio

logger = logging.getLogger(__name__)

class FeedIngestor:
    """Service for ingesting threat intelligence feeds and distributing to cloud services."""
    
    def __init__(self, cloud_service=None):
        self.cloud_service = cloud_service
        self.feeds = [
            {
                "name": "AbuseIPDB",
                "url": "https://api.abuseipdb.com/api/v2/blacklist",
                "type": "ip_blacklist",
                "active": True
            },
            {
                "name": "CISA KEV",
                "url": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
                "type": "vulnerability",
                "active": True
            },
            {
                "name": "Sample Threat Feed",
                "url": None,
                "type": "sample",
                "active": True
            }
        ]
        self.ingestion_stats = {
            "total_threats_processed": 0,
            "cloud_submissions": 0,
            "last_ingestion": None,
            "errors": 0
        }
    
    async def run_ingestion_cycle(self):
        """Run a complete ingestion cycle for all active feeds."""
        logger.info("🔄 Starting feed ingestion cycle...")
        
        try:
            ingestion_start = datetime.utcnow()
            threats_processed = 0
            
            for feed in self.feeds:
                if feed.get("active", False):
                    feed_threats = await self._ingest_feed(feed)
                    threats_processed += feed_threats
            
            # Update statistics
            self.ingestion_stats["total_threats_processed"] += threats_processed
            self.ingestion_stats["last_ingestion"] = ingestion_start.isoformat()
            
            logger.info(f"✅ Feed ingestion cycle completed - Processed {threats_processed} threats")
        except Exception as e:
            self.ingestion_stats["errors"] += 1
            logger.error(f"❌ Feed ingestion cycle failed: {e}")
    
    async def _ingest_feed(self, feed: Dict[str, Any]) -> int:
        """Ingest data from a single feed and return number of threats processed."""
        logger.info(f"📥 Ingesting feed: {feed['name']}")
        
        try:
            threats_processed = 0
            
            if feed["url"]:
                # In a real implementation, make HTTP request to feed URL
                # For now, simulate threat data ingestion
                sample_threats = await self._simulate_threat_data(feed)
                threats_processed = len(sample_threats)
                
                # Send threats to cloud services if available
                if self.cloud_service and sample_threats:
                    await self._send_threats_to_cloud(sample_threats, feed["name"])
            else:
                # Generate sample threat data for testing
                sample_threats = await self._simulate_threat_data(feed)
                threats_processed = len(sample_threats)
                
                if self.cloud_service and sample_threats:
                    await self._send_threats_to_cloud(sample_threats, feed["name"])
            
            logger.info(f"✅ Successfully ingested {threats_processed} threats from {feed['name']}")
            return threats_processed
            
        except Exception as e:
            logger.error(f"❌ Failed to ingest feed {feed['name']}: {e}")
            return 0
    
    async def _simulate_threat_data(self, feed: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate sample threat data for testing purposes."""
        await asyncio.sleep(0.1)  # Simulate processing time
        
        # Create sample threat data based on feed type
        if feed["type"] == "ip_blacklist":
            return [
                {
                    "value": "192.168.1.100",
                    "type": "ip",
                    "severity": "high",
                    "confidence": 0.95,
                    "description": f"Malicious IP detected by {feed['name']}",
                    "source": feed["name"],
                    "threat_score": 85,
                    "is_active": True,
                    "metadata": {"feed_type": "ip_blacklist", "detection_time": datetime.utcnow().isoformat()}
                },
                {
                    "value": "203.0.113.45",
                    "type": "ip",
                    "severity": "medium",
                    "confidence": 0.78,
                    "description": f"Suspicious IP activity from {feed['name']}",
                    "source": feed["name"],
                    "threat_score": 65,
                    "is_active": True,
                    "metadata": {"feed_type": "ip_blacklist", "detection_time": datetime.utcnow().isoformat()}
                }
            ]
        elif feed["type"] == "vulnerability":
            return [
                {
                    "value": "CVE-2024-0001",
                    "type": "cve",
                    "severity": "critical",
                    "confidence": 1.0,
                    "description": f"Critical vulnerability from {feed['name']}",
                    "source": feed["name"],
                    "threat_score": 95,
                    "is_active": True,
                    "metadata": {"feed_type": "vulnerability", "cve_score": 9.8, "detection_time": datetime.utcnow().isoformat()}
                }
            ]
        else:
            return [
                {
                    "value": "sample-threat-indicator",
                    "type": "sample",
                    "severity": "low",
                    "confidence": 0.5,
                    "description": f"Sample threat indicator from {feed['name']}",
                    "source": feed["name"],
                    "threat_score": 30,
                    "is_active": True,
                    "metadata": {"feed_type": "sample", "detection_time": datetime.utcnow().isoformat()}
                }
            ]
    
    async def _send_threats_to_cloud(self, threats: List[Dict[str, Any]], feed_name: str):
        """Send threat data to cloud services."""
        if not self.cloud_service:
            return
        
        try:
            for threat in threats:
                result = await self.cloud_service.send_threat_intelligence(threat)
                if result.get("overall_success", False):
                    self.ingestion_stats["cloud_submissions"] += 1
                    logger.debug(f"☁️ Threat sent to cloud: {threat.get('value', 'Unknown')}")
                else:
                    logger.warning(f"⚠️ Failed to send threat to cloud: {result}")
        except Exception as e:
            logger.error(f"❌ Error sending threats to cloud from {feed_name}: {e}")
    
    async def get_feed_status(self) -> Dict[str, Any]:
        """Get the status of all feeds."""
        return {
            "total_feeds": len(self.feeds),
            "active_feeds": len([f for f in self.feeds if f.get("active", False)]),
            "last_run": self.ingestion_stats.get("last_ingestion"),
            "statistics": self.ingestion_stats,
            "feeds": self.feeds,
            "cloud_integration": self.cloud_service is not None
        }
    
    def set_cloud_service(self, cloud_service):
        """Set the cloud service for threat data distribution."""
        self.cloud_service = cloud_service
        logger.info("☁️ Cloud service integration enabled for feed ingestor")
