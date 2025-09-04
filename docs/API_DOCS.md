# 📡 KRSN-RT2I API Documentation

## Overview

The KRSN-RT2I platform provides a comprehensive RESTful API built with FastAPI, offering real-time threat intelligence capabilities. This document covers all available endpoints, authentication methods, and usage examples.

## 🔐 Authentication

All API endpoints require authentication using an API key. Include the API key in the request header:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/endpoint
```

## 📊 Base URL

- **Local Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

All API endpoints are prefixed with `/api/v1/`

## 🛡️ Core Endpoints

### Health & Status

#### GET /health
Returns the current health status of the platform.

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-28T10:30:00Z",
  "version": "1.0.0",
  "uptime": "2d 14h 32m",
  "database": "connected",
  "feeds": {
    "active": 12,
    "last_update": "2025-01-28T10:25:00Z"
  }
}
```

#### GET /metrics
Prometheus-compatible metrics endpoint.

```bash
curl http://localhost:8000/metrics
```

### 🔍 Threat Intelligence

#### GET /api/v1/threats
Retrieve paginated list of threats.

**Parameters:**
- `page` (int, optional): Page number (default: 1)
- `size` (int, optional): Page size (default: 50, max: 500)
- `severity` (string, optional): Filter by severity (critical, high, medium, low)
- `source` (string, optional): Filter by threat source
- `date_from` (datetime, optional): Start date filter
- `date_to` (datetime, optional): End date filter

```bash
curl -H "X-API-Key: your-key" \
  "http://localhost:8000/api/v1/threats?page=1&size=10&severity=critical"
```

**Response:**
```json
{
  "total": 1250,
  "page": 1,
  "size": 10,
  "pages": 125,
  "items": [
    {
      "id": "threat_123456",
      "indicator": "192.168.1.100",
      "type": "ip",
      "severity": "critical",
      "score": 9.5,
      "first_seen": "2025-01-28T09:15:00Z",
      "last_seen": "2025-01-28T10:30:00Z",
      "sources": ["abuseipdb", "virustotal"],
      "tags": ["malware", "botnet", "c2"],
      "description": "Known malicious IP address associated with botnet activity",
      "recommendations": [
        "Block this IP address at your firewall",
        "Check for any connections to this IP in your logs",
        "Scan any systems that communicated with this IP"
      ]
    }
  ]
}
```

#### GET /api/v1/threats/{threat_id}
Get detailed information about a specific threat.

```bash
curl -H "X-API-Key: your-key" \
  http://localhost:8000/api/v1/threats/threat_123456
```

#### POST /api/v1/threats/search
Advanced threat search with multiple criteria.

```bash
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "192.168.1.100",
    "type": "ip",
    "include_context": true,
    "include_related": true
  }' \
  http://localhost:8000/api/v1/threats/search
```

**Response:**
```json
{
  "results": [
    {
      "indicator": "192.168.1.100",
      "type": "ip",
      "severity": "critical",
      "score": 9.5,
      "context": {
        "geolocation": {
          "country": "Unknown",
          "city": "Unknown",
          "asn": "AS12345"
        },
        "reputation": {
          "is_malicious": true,
          "confidence": 95,
          "last_updated": "2025-01-28T10:30:00Z"
        }
      },
      "related_threats": [
        {
          "indicator": "malicious-domain.com",
          "type": "domain",
          "relationship": "resolves_to"
        }
      ]
    }
  ],
  "total": 1,
  "query_time": "0.045s"
}
```

#### POST /api/v1/threats/bulk-analyze
Analyze multiple indicators simultaneously.

```bash
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "indicators": [
      "192.168.1.100",
      "malicious-domain.com",
      "d41d8cd98f00b204e9800998ecf8427e"
    ]
  }' \
  http://localhost:8000/api/v1/threats/bulk-analyze
```

### 📊 Dashboard & Analytics

#### GET /api/v1/dashboard/summary
Get dashboard summary statistics.

```bash
curl -H "X-API-Key: your-key" \
  http://localhost:8000/api/v1/dashboard/summary
```

**Response:**
```json
{
  "total_threats": 15420,
  "active_threats": 234,
  "critical_alerts": 12,
  "feeds_active": 15,
  "last_update": "2025-01-28T10:30:00Z",
  "threat_breakdown": {
    "critical": 45,
    "high": 189,
    "medium": 567,
    "low": 234
  },
  "top_threat_types": [
    {"type": "malicious_ip", "count": 5432},
    {"type": "malware_hash", "count": 3210},
    {"type": "phishing_domain", "count": 2876}
  ]
}
```

#### GET /api/v1/dashboard/trends
Get threat trends and time-series data.

```bash
curl -H "X-API-Key: your-key" \
  "http://localhost:8000/api/v1/dashboard/trends?period=24h&granularity=1h"
```

#### GET /api/v1/dashboard/geo-threats
Get geographic distribution of threats.

```bash
curl -H "X-API-Key: your-key" \
  http://localhost:8000/api/v1/dashboard/geo-threats
```

### 🚨 Alerts & Notifications

#### GET /api/v1/alerts
Retrieve active alerts.

```bash
curl -H "X-API-Key: your-key" \
  "http://localhost:8000/api/v1/alerts?status=active&severity=critical"
```

#### POST /api/v1/alerts/{alert_id}/acknowledge
Acknowledge an alert.

```bash
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"acknowledged_by": "security_analyst", "notes": "Investigating"}' \
  http://localhost:8000/api/v1/alerts/alert_123/acknowledge
```

#### POST /api/v1/alerts/subscribe
Subscribe to alert notifications.

```bash
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "analyst@company.com",
    "severity_levels": ["critical", "high"],
    "notification_types": ["email", "webhook"]
  }' \
  http://localhost:8000/api/v1/alerts/subscribe
```

### 🔍 Investigation & Hunting

#### POST /api/v1/investigate/ip
Deep investigation of an IP address.

```bash
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"ip": "192.168.1.100", "include_passive_dns": true}' \
  http://localhost:8000/api/v1/investigate/ip
```

#### POST /api/v1/investigate/domain
Domain reputation and analysis.

```bash
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"domain": "suspicious-domain.com", "include_subdomains": true}' \
  http://localhost:8000/api/v1/investigate/domain
```

#### POST /api/v1/investigate/hash
File hash analysis and malware detection.

```bash
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"hash": "d41d8cd98f00b204e9800998ecf8427e", "hash_type": "md5"}' \
  http://localhost:8000/api/v1/investigate/hash
```

### 🤖 Machine Learning & Prediction

#### POST /api/v1/ml/predict
Get ML-based threat predictions.

```bash
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "ip": "192.168.1.100",
      "port": 80,
      "protocol": "HTTP",
      "geolocation": "US"
    }
  }' \
  http://localhost:8000/api/v1/ml/predict
```

#### GET /api/v1/ml/models
List available ML models and their status.

```bash
curl -H "X-API-Key: your-key" \
  http://localhost:8000/api/v1/ml/models
```

### 📈 Feeds & Sources

#### GET /api/v1/feeds
List all configured threat intelligence feeds.

```bash
curl -H "X-API-Key: your-key" \
  http://localhost:8000/api/v1/feeds
```

#### POST /api/v1/feeds/{feed_id}/refresh
Manually refresh a specific feed.

```bash
curl -X POST \
  -H "X-API-Key: your-key" \
  http://localhost:8000/api/v1/feeds/abuseipdb/refresh
```

## 🔌 WebSocket Endpoints

### Real-time Threat Stream

Connect to the WebSocket endpoint for real-time threat updates:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/threats');

ws.onmessage = function(event) {
    const threat = JSON.parse(event.data);
    console.log('New threat:', threat);
};

ws.onopen = function(event) {
    // Subscribe to specific threat types
    ws.send(JSON.stringify({
        "action": "subscribe",
        "filters": {
            "severity": ["critical", "high"],
            "types": ["ip", "domain"]
        }
    }));
};
```

### Live Dashboard Updates

```javascript
const dashboardWs = new WebSocket('ws://localhost:8000/ws/dashboard');

dashboardWs.onmessage = function(event) {
    const update = JSON.parse(event.data);
    updateDashboardMetrics(update);
};
```

## 📝 Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Default**: 100 requests per minute per API key
- **Burst**: Up to 10 requests per second
- **Headers**: Rate limit information is included in response headers

```bash
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1643123456
```

## ❌ Error Handling

The API uses standard HTTP status codes and returns detailed error information:

```json
{
  "error": {
    "code": "INVALID_INDICATOR",
    "message": "The provided indicator format is invalid",
    "details": {
      "indicator": "invalid-ip-format",
      "expected_format": "IPv4 or IPv6 address"
    },
    "timestamp": "2025-01-28T10:30:00Z",
    "request_id": "req_123456789"
  }
}
```

### Common Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or missing API key
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error

## 🔧 SDK Examples

### Python SDK

```python
import requests
from typing import Dict, List, Optional

class KRSN_RT2I_Client:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'X-API-Key': api_key})
    
    def search_threats(self, query: str, threat_type: str = None) -> Dict:
        """Search for threats matching the query."""
        payload = {'query': query}
        if threat_type:
            payload['type'] = threat_type
        
        response = self.session.post(
            f"{self.base_url}/api/v1/threats/search",
            json=payload
        )
        return response.json()
    
    def get_dashboard_summary(self) -> Dict:
        """Get dashboard summary statistics."""
        response = self.session.get(
            f"{self.base_url}/api/v1/dashboard/summary"
        )
        return response.json()
    
    def bulk_analyze(self, indicators: List[str]) -> Dict:
        """Analyze multiple indicators."""
        response = self.session.post(
            f"{self.base_url}/api/v1/threats/bulk-analyze",
            json={'indicators': indicators}
        )
        return response.json()

# Usage example
client = KRSN_RT2I_Client('http://localhost:8000', 'your-api-key')
results = client.search_threats('192.168.1.100', 'ip')
```

### JavaScript/Node.js SDK

```javascript
class KRSN_RT2I_Client {
    constructor(baseUrl, apiKey) {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.apiKey = apiKey;
    }
    
    async request(method, endpoint, data = null) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            method,
            headers: {
                'X-API-Key': this.apiKey,
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            config.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, config);
        return await response.json();
    }
    
    async searchThreats(query, type = null) {
        const payload = { query };
        if (type) payload.type = type;
        
        return await this.request('POST', '/api/v1/threats/search', payload);
    }
    
    async getDashboardSummary() {
        return await this.request('GET', '/api/v1/dashboard/summary');
    }
    
    async bulkAnalyze(indicators) {
        return await this.request('POST', '/api/v1/threats/bulk-analyze', {
            indicators
        });
    }
}

// Usage example
const client = new KRSN_RT2I_Client('http://localhost:8000', 'your-api-key');
const results = await client.searchThreats('192.168.1.100', 'ip');
```

## 🧪 Testing the API

### Using curl

```bash
# Test authentication
curl -H "X-API-Key: your-key" http://localhost:8000/api/v1/dashboard/summary

# Test threat search
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"query": "8.8.8.8", "type": "ip"}' \
  http://localhost:8000/api/v1/threats/search

# Test bulk analysis
curl -X POST \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"indicators": ["8.8.8.8", "1.1.1.1"]}' \
  http://localhost:8000/api/v1/threats/bulk-analyze
```

### Using Postman

Import the provided Postman collection:
1. Download `KRSN-RT2I-API.postman_collection.json`
2. Import into Postman
3. Set environment variables:
   - `base_url`: http://localhost:8000
   - `api_key`: your-api-key

## 📚 Additional Resources

- **Interactive API Docs**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **Redoc Documentation**: http://localhost:8000/redoc
- **API Status Page**: http://localhost:8000/status

---

For more information and support, visit our [GitHub repository](https://github.com/STLR-TRAJ/KRSN-RT2I) or contact our support team.
