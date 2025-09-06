"""
Remote Elasticsearch Cloud integration service for KRSN-RT2I.
"""

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Text, Keyword, Date, Integer, Float, Boolean, connections
from typing import Dict, Any, List, Optional
import logging
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ElasticsearchCloudService:
    """Service for integrating with Elasticsearch Cloud."""
    
    def __init__(self):
        self.hosts = os.getenv("ELASTICSEARCH_HOSTS", "").split(",")
        self.username = os.getenv("ELASTICSEARCH_USERNAME", "")
        self.password = os.getenv("ELASTICSEARCH_PASSWORD", "")
        self.api_key = os.getenv("ELASTICSEARCH_API_KEY", "")
        self.index_prefix = os.getenv("ELASTICSEARCH_INDEX_PREFIX", "rtip")
        self.es_client = None
        
    def connect(self) -> bool:
        """Connect to Elasticsearch Cloud."""
        try:
            logger.info("🔗 Connecting to Elasticsearch Cloud...")
            
            # Configure authentication
            auth_config = {}
            if self.api_key:
                # Use API key authentication
                auth_config["api_key"] = self.api_key.strip('"')
            elif self.username and self.password:
                # Use basic authentication
                auth_config["basic_auth"] = (self.username, self.password)
            
            # Create Elasticsearch client
            self.es_client = Elasticsearch(
                hosts=self.hosts,
                **auth_config,
                verify_certs=True,
                ssl_show_warn=False,
                request_timeout=30,
                retry_on_timeout=True,
                max_retries=3
            )
            
            # Test connection
            if self.es_client.ping():
                cluster_info = self.es_client.info()
                logger.info(f"✅ Connected to Elasticsearch Cloud")
                logger.info(f"📊 Cluster: {cluster_info['cluster_name']}")
                logger.info(f"🏷️ Version: {cluster_info['version']['number']}")
                
                # Set up default connection for elasticsearch-dsl
                connections.add_connection('default', self.es_client)
                
                return True
            else:
                logger.error("❌ Elasticsearch ping failed")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to connect to Elasticsearch Cloud: {e}")
            return False
    
    async def create_index_template(self) -> bool:
        """Create index template for threat intelligence data."""
        try:
            if not self.es_client:
                if not self.connect():
                    return False
            
            template_name = f"{self.index_prefix}-template"
            index_pattern = f"{self.index_prefix}-*"
            
            template_body = {
                "index_patterns": [index_pattern],
                "template": {
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 1
                    },
                    "mappings": {
                        "properties": {
                            "timestamp": {"type": "date"},
                            "indicator_value": {"type": "keyword"},
                            "indicator_type": {"type": "keyword"},
                            "severity": {"type": "keyword"},
                            "confidence": {"type": "float"},
                            "source": {"type": "keyword"},
                            "description": {"type": "text"},
                            "threat_score": {"type": "integer"},
                            "is_active": {"type": "boolean"},
                            "metadata": {"type": "object"},
                            "geolocation": {
                                "properties": {
                                    "country": {"type": "keyword"},
                                    "city": {"type": "keyword"},
                                    "coordinates": {"type": "geo_point"}
                                }
                            }
                        }
                    }
                }
            }
            
            # Create or update template
            self.es_client.indices.put_index_template(
                name=template_name,
                body=template_body
            )
            
            logger.info(f"✅ Created Elasticsearch index template: {template_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to create index template: {e}")
            return False
    
    async def index_threat_data(self, threat_data: Dict[str, Any]) -> bool:
        """Index threat intelligence data to Elasticsearch Cloud."""
        try:
            if not self.es_client:
                if not self.connect():
                    return False
            
            # Prepare document
            doc = {
                "timestamp": datetime.utcnow(),
                "indicator_value": threat_data.get("value", ""),
                "indicator_type": threat_data.get("type", ""),
                "severity": threat_data.get("severity", "medium"),
                "confidence": threat_data.get("confidence", 0.0),
                "source": threat_data.get("source", "krsn-rt2i"),
                "description": threat_data.get("description", ""),
                "threat_score": threat_data.get("threat_score", 0),
                "is_active": threat_data.get("is_active", True),
                "metadata": threat_data.get("metadata", {})
            }
            
            # Generate index name with date
            index_name = f"{self.index_prefix}-{datetime.now().strftime('%Y.%m.%d')}"
            
            # Index document
            response = self.es_client.index(
                index=index_name,
                body=doc
            )
            
            logger.info(f"✅ Indexed threat data to Elasticsearch: {response['_id']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to index threat data: {e}")
            return False
    
    async def search_threats(self, query: str, size: int = 100) -> List[Dict]:
        """Search for threats in Elasticsearch Cloud."""
        try:
            if not self.es_client:
                if not self.connect():
                    return []
            
            # Build search query
            search_body = {
                "query": {
                    "bool": {
                        "should": [
                            {"match": {"indicator_value": query}},
                            {"match": {"description": query}},
                            {"term": {"source.keyword": query}}
                        ],
                        "minimum_should_match": 1
                    }
                },
                "sort": [
                    {"timestamp": {"order": "desc"}}
                ],
                "size": size
            }
            
            # Execute search across all indices
            index_pattern = f"{self.index_prefix}-*"
            response = self.es_client.search(
                index=index_pattern,
                body=search_body
            )
            
            # Extract results
            results = []
            for hit in response['hits']['hits']:
                result = hit['_source']
                result['_id'] = hit['_id']
                result['_score'] = hit['_score']
                results.append(result)
            
            logger.info(f"🔍 Elasticsearch search returned {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Elasticsearch search failed: {e}")
            return []
    
    async def get_threat_statistics(self) -> Dict[str, Any]:
        """Get threat intelligence statistics from Elasticsearch."""
        try:
            if not self.es_client:
                if not self.connect():
                    return {}
            
            index_pattern = f"{self.index_prefix}-*"
            
            # Aggregation query
            agg_body = {
                "size": 0,
                "aggs": {
                    "total_threats": {"value_count": {"field": "indicator_value.keyword"}},
                    "severity_breakdown": {
                        "terms": {"field": "severity.keyword"}
                    },
                    "type_breakdown": {
                        "terms": {"field": "indicator_type.keyword"}
                    },
                    "source_breakdown": {
                        "terms": {"field": "source.keyword"}
                    },
                    "recent_threats": {
                        "date_histogram": {
                            "field": "timestamp",
                            "calendar_interval": "1d",
                            "order": {"_key": "desc"}
                        }
                    }
                }
            }
            
            response = self.es_client.search(
                index=index_pattern,
                body=agg_body
            )
            
            # Process aggregations
            aggs = response['aggregations']
            stats = {
                "total_threats": aggs['total_threats']['value'],
                "by_severity": {bucket['key']: bucket['doc_count'] 
                              for bucket in aggs['severity_breakdown']['buckets']},
                "by_type": {bucket['key']: bucket['doc_count'] 
                           for bucket in aggs['type_breakdown']['buckets']},
                "by_source": {bucket['key']: bucket['doc_count'] 
                             for bucket in aggs['source_breakdown']['buckets']},
                "recent_activity": [
                    {
                        "date": bucket['key_as_string'],
                        "count": bucket['doc_count']
                    } 
                    for bucket in aggs['recent_threats']['buckets'][:7]
                ],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Failed to get Elasticsearch statistics: {e}")
            return {}
    
    async def get_connection_status(self) -> Dict[str, Any]:
        """Get Elasticsearch Cloud connection status."""
        try:
            if not self.es_client:
                connected = self.connect()
            else:
                connected = self.es_client.ping()
            
            if connected:
                cluster_info = self.es_client.info()
                cluster_health = self.es_client.cluster.health()
                
                return {
                    "status": "connected",
                    "cluster_name": cluster_info.get("cluster_name", "Unknown"),
                    "version": cluster_info.get("version", {}).get("number", "Unknown"),
                    "health": cluster_health.get("status", "unknown"),
                    "nodes": cluster_health.get("number_of_nodes", 0),
                    "indices": cluster_health.get("active_primary_shards", 0),
                    "timestamp": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "status": "disconnected",
                    "error": "Failed to ping cluster",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
