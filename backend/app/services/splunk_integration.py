"""
Remote Splunk Cloud integration service for KRSN-RT2I.
"""

import splunklib.client as client
import splunklib.results as results
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class SplunkCloudService:
    """Service for integrating with Splunk Cloud."""
    
    def __init__(self):
        self.splunk_url = os.getenv("SPLUNK_URL", "").replace("https://", "")
        self.username = os.getenv("SPLUNK_USERNAME", "")
        self.password = os.getenv("SPLUNK_PASSWORD", "")
        self.token = os.getenv("SPLUNK_TOKEN", "")
        self.index = os.getenv("SPLUNK_INDEX", "rtip_threats")
        self.service = None
        
    def connect(self) -> bool:
        """Connect to Splunk Cloud instance."""
        try:
            logger.info("🔗 Connecting to Splunk Cloud...")
            
            # Connect using token authentication
            if self.token:
                self.service = client.connect(
                    host=self.splunk_url,
                    port=8089,
                    token=self.token,
                    scheme="https"
                )
            else:
                # Fallback to username/password
                self.service = client.connect(
                    host=self.splunk_url,
                    port=8089,
                    username=self.username,
                    password=self.password,
                    scheme="https"
                )
            
            # Test connection
            apps = self.service.apps
            logger.info(f"✅ Connected to Splunk Cloud: {self.splunk_url}")
            logger.info(f"📊 Available apps: {len(apps)}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Splunk Cloud: {e}")
            return False
    
    def send_threat_data(self, threat_data: Dict[str, Any]) -> bool:
        """Send threat intelligence data to Splunk Cloud."""
        try:
            if not self.service:
                if not self.connect():
                    return False
            
            # Get the index
            myindex = self.service.indexes[self.index]
            
            # Prepare event data
            event_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "source": "krsn-rt2i",
                "sourcetype": "threat_intelligence",
                "event": threat_data
            }
            
            # Submit event
            myindex.submit(json.dumps(event_data))
            
            logger.info(f"✅ Threat data sent to Splunk Cloud index: {self.index}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send threat data to Splunk: {e}")
            return False
    
    def search_threats(self, query: str, earliest_time: str = "-24h") -> List[Dict]:
        """Search for threats in Splunk Cloud."""
        try:
            if not self.service:
                if not self.connect():
                    return []
            
            # Build search query
            search_query = f'search index={self.index} {query} earliest={earliest_time}'
            
            # Execute search
            job = self.service.jobs.create(search_query)
            
            # Wait for job to complete
            while not job.is_done():
                pass
            
            # Get results
            result_list = []
            for result in results.ResultsReader(job.results()):
                if isinstance(result, dict):
                    result_list.append(result)
            
            logger.info(f"🔍 Splunk search returned {len(result_list)} results")
            return result_list
            
        except Exception as e:
            logger.error(f"❌ Splunk search failed: {e}")
            return []
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get Splunk Cloud connection status."""
        try:
            if not self.service:
                connected = self.connect()
            else:
                connected = True
                
            if connected:
                info = self.service.info
                return {
                    "status": "connected",
                    "server_name": info.get("serverName", "Unknown"),
                    "version": info.get("version", "Unknown"),
                    "index": self.index,
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "status": "disconnected",
                    "error": "Failed to establish connection",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    def create_alert(self, alert_name: str, search_query: str, description: str = "") -> bool:
        """Create a saved search/alert in Splunk Cloud."""
        try:
            if not self.service:
                if not self.connect():
                    return False
            
            # Create saved search
            saved_search = self.service.saved_searches.create(
                alert_name,
                search=f'index={self.index} {search_query}',
                dispatch_earliest_time="-15m",
                dispatch_latest_time="now"
            )
            
            logger.info(f"✅ Created Splunk alert: {alert_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create Splunk alert: {e}")
            return False
