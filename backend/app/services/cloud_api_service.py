"""
Cloud API integration service for KRSN-RT2I.
Coordinates Splunk Cloud and Elasticsearch Cloud integrations.
"""

from typing import Dict, Any, List, Optional
import logging
import asyncio
from datetime import datetime
import json

from .splunk_integration import SplunkCloudService
from .elasticsearch_integration import ElasticsearchCloudService

logger = logging.getLogger(__name__)

class CloudAPIService:
    """Service for managing cloud API integrations."""
    
    def __init__(self):
        self.splunk = SplunkCloudService()
        self.elasticsearch = ElasticsearchCloudService()
        self.is_initialized = False
    
    async def initialize(self) -> bool:
        """Initialize all cloud service connections."""
        try:
            logger.info("🚀 Initializing cloud API services...")
            
            # Connect to services in parallel
            splunk_task = asyncio.create_task(self._connect_splunk())
            elastic_task = asyncio.create_task(self._connect_elasticsearch())
            
            splunk_connected, elastic_connected = await asyncio.gather(
                splunk_task, elastic_task, return_exceptions=True
            )
            
            self.is_initialized = True
            
            # Log connection status
            if isinstance(splunk_connected, bool) and splunk_connected:
                logger.info("✅ Splunk Cloud connected")
            else:
                logger.warning(f"⚠️ Splunk Cloud connection failed: {splunk_connected}")
            
            if isinstance(elastic_connected, bool) and elastic_connected:
                logger.info("✅ Elasticsearch Cloud connected")
            else:
                logger.warning(f"⚠️ Elasticsearch Cloud connection failed: {elastic_connected}")
            
            # Initialize Elasticsearch index template
            if isinstance(elastic_connected, bool) and elastic_connected:
                await self.elasticsearch.create_index_template()
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize cloud services: {e}")
            return False
    
    async def _connect_splunk(self) -> bool:
        """Connect to Splunk Cloud."""
        try:
            return await asyncio.to_thread(self.splunk.connect)
        except Exception as e:
            logger.error(f"❌ Splunk connection error: {e}")
            return False
    
    async def _connect_elasticsearch(self) -> bool:
        """Connect to Elasticsearch Cloud."""
        try:
            return self.elasticsearch.connect()
        except Exception as e:
            logger.error(f"❌ Elasticsearch connection error: {e}")
            return False
    
    async def send_threat_intelligence(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send threat intelligence to both cloud services."""
        if not self.is_initialized:
            await self.initialize()
        
        results = {
            "threat_id": threat_data.get("id", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "services": {}
        }
        
        # Send to services in parallel
        tasks = []
        
        # Splunk task
        async def send_to_splunk():
            try:
                success = await asyncio.to_thread(
                    self.splunk.send_threat_data, threat_data
                )
                return {"service": "splunk", "success": success}
            except Exception as e:
                logger.error(f"❌ Splunk send error: {e}")
                return {"service": "splunk", "success": False, "error": str(e)}
        
        # Elasticsearch task
        async def send_to_elasticsearch():
            try:
                success = await self.elasticsearch.index_threat_data(threat_data)
                return {"service": "elasticsearch", "success": success}
            except Exception as e:
                logger.error(f"❌ Elasticsearch send error: {e}")
                return {"service": "elasticsearch", "success": False, "error": str(e)}
        
        tasks = [send_to_splunk(), send_to_elasticsearch()]
        service_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in service_results:
            if isinstance(result, dict):
                service_name = result["service"]
                results["services"][service_name] = {
                    "success": result["success"],
                    "error": result.get("error")
                }
            else:
                logger.error(f"❌ Service task failed: {result}")
        
        # Overall success status
        results["overall_success"] = all(
            svc.get("success", False) for svc in results["services"].values()
        )
        
        logger.info(f"📤 Threat intelligence sent - Overall: {results['overall_success']}")
        return results
    
    async def search_threats(self, query: str, size: int = 100) -> Dict[str, Any]:
        """Search for threats across all cloud services."""
        if not self.is_initialized:
            await self.initialize()
        
        results = {
            "query": query,
            "timestamp": datetime.utcnow().isoformat(),
            "results": {}
        }
        
        # Search services in parallel
        async def search_splunk():
            try:
                return await asyncio.to_thread(
                    self.splunk.search_threats, query, size
                )
            except Exception as e:
                logger.error(f"❌ Splunk search error: {e}")
                return []
        
        async def search_elasticsearch():
            try:
                return await self.elasticsearch.search_threats(query, size)
            except Exception as e:
                logger.error(f"❌ Elasticsearch search error: {e}")
                return []
        
        splunk_results, elastic_results = await asyncio.gather(
            search_splunk(), search_elasticsearch(), return_exceptions=True
        )
        
        # Process results
        results["results"]["splunk"] = {
            "count": len(splunk_results) if isinstance(splunk_results, list) else 0,
            "data": splunk_results if isinstance(splunk_results, list) else []
        }
        
        results["results"]["elasticsearch"] = {
            "count": len(elastic_results) if isinstance(elastic_results, list) else 0,
            "data": elastic_results if isinstance(elastic_results, list) else []
        }
        
        # Combine and deduplicate results
        combined_results = []
        seen_indicators = set()
        
        for source_results in [splunk_results, elastic_results]:
            if isinstance(source_results, list):
                for item in source_results:
                    indicator = item.get("indicator_value", "") or item.get("value", "")
                    if indicator and indicator not in seen_indicators:
                        seen_indicators.add(indicator)
                        combined_results.append(item)
        
        results["combined"] = {
            "count": len(combined_results),
            "data": combined_results[:size]  # Limit to requested size
        }
        
        logger.info(f"🔍 Search completed - Combined: {len(combined_results)} results")
        return results
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status from all cloud services."""
        if not self.is_initialized:
            await self.initialize()
        
        status = {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_health": "unknown",
            "services": {}
        }
        
        # Get service statuses in parallel
        async def get_splunk_status():
            try:
                return await asyncio.to_thread(self.splunk.get_connection_status)
            except Exception as e:
                logger.error(f"❌ Splunk status error: {e}")
                return {"status": "error", "error": str(e)}
        
        async def get_elasticsearch_status():
            try:
                return await self.elasticsearch.get_connection_status()
            except Exception as e:
                logger.error(f"❌ Elasticsearch status error: {e}")
                return {"status": "error", "error": str(e)}
        
        splunk_status, elastic_status = await asyncio.gather(
            get_splunk_status(), get_elasticsearch_status(), return_exceptions=True
        )
        
        # Process statuses
        status["services"]["splunk"] = splunk_status if isinstance(splunk_status, dict) else {
            "status": "error", "error": str(splunk_status)
        }
        
        status["services"]["elasticsearch"] = elastic_status if isinstance(elastic_status, dict) else {
            "status": "error", "error": str(elastic_status)
        }
        
        # Determine overall health
        service_statuses = [
            svc.get("status", "error") for svc in status["services"].values()
        ]
        
        if all(s == "connected" for s in service_statuses):
            status["overall_health"] = "healthy"
        elif any(s == "connected" for s in service_statuses):
            status["overall_health"] = "degraded"
        else:
            status["overall_health"] = "unhealthy"
        
        return status
    
    async def get_threat_statistics(self) -> Dict[str, Any]:
        """Get combined threat statistics from all services."""
        if not self.is_initialized:
            await self.initialize()
        
        stats = {
            "timestamp": datetime.utcnow().isoformat(),
            "services": {},
            "combined": {}
        }
        
        # Get statistics in parallel
        async def get_elastic_stats():
            try:
                return await self.elasticsearch.get_threat_statistics()
            except Exception as e:
                logger.error(f"❌ Elasticsearch stats error: {e}")
                return {}
        
        # Currently, Splunk integration doesn't have statistics method
        # We'll implement that later if needed
        elastic_stats = await get_elastic_stats()
        
        stats["services"]["elasticsearch"] = elastic_stats
        stats["combined"] = elastic_stats  # For now, just use Elasticsearch stats
        
        return stats
    
    async def create_alert(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create alerts in both cloud services."""
        if not self.is_initialized:
            await self.initialize()
        
        results = {
            "alert_id": alert_data.get("id", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "services": {}
        }
        
        # Create Splunk alert
        try:
            splunk_success = await asyncio.to_thread(
                self.splunk.create_alert,
                alert_data.get("name", "RTIP Alert"),
                alert_data.get("search_query", "*"),
                alert_data.get("description", "Alert from RTIP system")
            )
            results["services"]["splunk"] = {"success": splunk_success}
        except Exception as e:
            logger.error(f"❌ Splunk alert creation error: {e}")
            results["services"]["splunk"] = {"success": False, "error": str(e)}
        
        # For Elasticsearch, we could create a watcher or similar
        # For now, we'll just index the alert data
        try:
            elastic_success = await self.elasticsearch.index_threat_data({
                **alert_data,
                "type": "alert",
                "is_alert": True
            })
            results["services"]["elasticsearch"] = {"success": elastic_success}
        except Exception as e:
            logger.error(f"❌ Elasticsearch alert indexing error: {e}")
            results["services"]["elasticsearch"] = {"success": False, "error": str(e)}
        
        results["overall_success"] = all(
            svc.get("success", False) for svc in results["services"].values()
        )
        
        return results
