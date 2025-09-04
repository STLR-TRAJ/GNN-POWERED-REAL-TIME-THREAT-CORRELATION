# �️ KRSN-RT2I Complete Installation Guide

**KRSN-RT2I: Advanced Real-Time Threat Intelligence Platform**

Complete setup guide for the KRSN-RT2I (Knowledge-Rich Security Network - Real-Time Threat Intelligence) platform. This enterprise-grade cybersecurity solution provides AI-powered threat detection, real-time analysis, and comprehensive threat intelligence capabilities.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Setup](#pre-installation-setup)
4. [Quick Start (Docker)](#quick-start-docker)
5. [Manual Development Setup](#manual-development-setup)
6. [AI Model Configuration](#ai-model-configuration)
7. [Platform Configuration](#platform-configuration)
8. [Post-Installation Verification](#post-installation-verification)
9. [Advanced Configuration](#advanced-configuration)
10. [Troubleshooting](#troubleshooting)
11. [Maintenance & Updates](#maintenance--updates)
12. [Support & Documentation](#support--documentation)

---

## 🌟 Project Overview

**KRSN-RT2I** is an enterprise-grade, AI-powered threat intelligence platform that provides:

- 🧠 **Advanced AI/ML Analysis**: Ensemble models with Random Forest, Neural Networks, and Anomaly Detection
- ⚡ **Real-Time Processing**: Sub-100ms threat detection and correlation
- 🎨 **Modern Interface**: Next.js 15 + React 19 with real-time dashboards
- 🔄 **Live Data Processing**: Real-time threat analysis with 39 network features
- 🐳 **Cloud-Native**: Docker-first, Kubernetes-ready architecture
- 📡 **Multi-Source Intelligence**: Integration with external threat feeds

### 🎯 Key Features

- **AI Threat Detection**: 95.7% accuracy ensemble model
- **Real-time Dashboards**: Live threat visualization
- **API-First Design**: RESTful endpoints for integration
- **Background Processing**: Automated threat analysis
- **Enterprise Security**: JWT, RBAC, encryption
- **Scalable Architecture**: Microservices with horizontal scaling

---

## 💻 System Requirements

### 🖥️ Minimum Requirements
- **Operating System**: Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)
- **CPU**: 4 cores (Intel i5 or AMD Ryzen 5 equivalent)
- **RAM**: 8 GB (16 GB recommended for AI training)
- **Storage**: 20 GB free space (50 GB for full datasets)
- **Network**: Broadband internet connection (10+ Mbps)

### 🚀 Recommended Requirements (Production)
- **CPU**: 8+ cores (Intel i7/i9 or AMD Ryzen 7/9)
- **RAM**: 16-32 GB (for optimal AI performance)
- **Storage**: 100+ GB SSD (for datasets and logs)
- **Network**: High-speed internet (50+ Mbps)
- **GPU**: Optional - NVIDIA GPU with CUDA 11.8+ for enhanced AI performance

### 🔧 Software Prerequisites
- **Node.js**: 18.0+ (for frontend development)
- **Python**: 3.11+ (for backend and AI models)
- **Docker**: 24.0+ (recommended installation method)
- **Git**: 2.40+ (for version control)

---

## �️ Pre-Installation Setup

### �🐳 Installing Docker (Recommended Method)

Docker provides the easiest and most reliable way to run KRSN-RT2I. Follow the instructions for your operating system:

#### Windows Installation

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"
   - Ensure WSL2 is enabled

2. **Install Docker Desktop**
   ```powershell
   # Run the installer as Administrator
   # Enable WSL2 integration when prompted
   # Restart your computer after installation
   ```

3. **Verify Installation**
   ```powershell
   docker --version
   docker compose version
   ```

#### macOS Installation

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Choose appropriate version (Intel or Apple Silicon)

2. **Install and Verify**
   ```bash
   # Install via Homebrew (alternative)
   brew install --cask docker
   
   # Verify installation
   docker --version
   docker compose version
   ```

#### Linux Installation (Ubuntu/Debian)

```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group (optional)
sudo usermod -aG docker $USER
# Log out and back in for changes to take effect

# Verify installation
docker --version
docker compose version
```

### 📥 Downloading KRSN-RT2I

#### Method 1: Git Clone (Recommended)

```bash
# Clone the repository
git clone https://github.com/STLR-TRAJ/GNN-POWERED-REAL-TIME-THREAT-CORRELATION.git
cd GNN-POWERED-REAL-TIME-THREAT-CORRELATION

# Verify project structure
ls -la
```

#### Method 2: Download ZIP

1. Visit: https://github.com/STLR-TRAJ/GNN-POWERED-REAL-TIME-THREAT-CORRELATION
2. Click "Code" → "Download ZIP"
3. Extract to your preferred directory
4. Navigate to the extracted folder

---

## 🚀 Quick Start (Docker)

### 🐳 One-Command Deployment

The fastest way to get KRSN-RT2I running:

```bash
# Navigate to project directory
cd GNN-POWERED-REAL-TIME-THREAT-CORRELATION

# Quick start with default configuration
docker compose up -d

# Wait for services to initialize (2-3 minutes)
echo "⏳ Waiting for services to start..."
sleep 120

# Check service status
docker compose ps
```

### 🔍 Access the Platform

After deployment, access the platform:

- 🖥️ **Web Dashboard**: http://localhost:3000
- 🔌 **API Documentation**: http://localhost:8000/docs
- ⚡ **API Health Check**: http://localhost:8000/health

### 📊 First-Time Setup Verification

```bash
# Check if all services are healthy
docker compose ps

# Expected output:
# NAME                                  COMMAND                  SERVICE    STATUS     PORTS
# gnn-powered-real-time-threat-backend  "uvicorn app.main:ap…"   backend    Up (healthy) 0.0.0.0:8000->8000/tcp
# gnn-powered-real-time-threat-frontend "nginx -g 'daemon of…"   frontend   Up (healthy) 0.0.0.0:3000->80/tcp

# View logs
docker compose logs -f
```

---

## ⚙️ Manual Development Setup

For developers who want to run KRSN-RT2I in development mode:

### 🐍 Backend Setup (Python/FastAPI)

```bash
# Navigate to project directory
cd GNN-POWERED-REAL-TIME-THREAT-CORRELATION

# Create Python virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Create data directory
mkdir -p backend/data

# Start the backend server
python backend/start_server.py
```

The backend will be available at: http://localhost:8000

### 🎨 Frontend Setup (Next.js/React)

```bash
# Open new terminal in project directory
cd GNN-POWERED-REAL-TIME-THREAT-CORRELATION

# Install Node.js dependencies
npm install
# or with pnpm (recommended):
pnpm install

# Start development server
npm run dev
# or with pnpm:
pnpm dev
```

The frontend will be available at: http://localhost:3000

### 🔄 Alternative Vue.js Frontend (Optional)

```bash
# Navigate to Vue.js frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The Vue.js frontend will be available at: http://localhost:5173

---

## 🧠 AI Model Configuration

### 🤖 Pre-trained Models

KRSN-RT2I comes with pre-trained AI models located in the `models/` directory:

- `random_forest_threat_detector.pkl` - Random Forest classifier
- `neural_network_threat_detector.pkl` - Neural Network model  
- `anomaly_detector_threat_detector.pkl` - Isolation Forest for anomaly detection
- `scaler.pkl` - Feature scaler for data preprocessing
- `training_results.json` - Model performance metrics

### 🚀 Quick AI System Test

```bash
# Test the AI threat detection system
python scripts/test_system.py

# Expected output:
# 🧠 AI Model: TRAINED and OPERATIONAL
# ⚡ Real-time Detection: READY
# 📊 Batch Analysis: READY  
# 🎉 KRSN-RT2I Threat Detection System - OPERATIONAL!
```

### 🔄 Retraining Models (Optional)

To retrain models with your own data:

```bash
# Train with custom dataset
python scripts/krsn_threat_detector.py --train --dataset ./data/your_dataset.csv

# The training process will:
# 1. Load and preprocess your data
# 2. Train Random Forest, Neural Network, and Anomaly Detection models
# 3. Save trained models to the models/ directory
# 4. Generate performance reports
```

### 📊 Model Performance Verification

```bash
# Get detailed model performance metrics
python -c "
from scripts.krsn_threat_detector import load_threat_detector
detector = load_threat_detector()
print(detector.get_model_status())
"

# Expected metrics:
# Random Forest Accuracy: >92%
# Neural Network Accuracy: >89%  
# Ensemble Accuracy: >94%
# Response Time: <100ms
```

---

## 🔧 Platform Configuration

### 📧 Environment Variables

Create a `.env` file in the project root (copy from `.env.example` if available):

```env
# ===================
# Core Configuration
# ===================
DATABASE_URL=sqlite:///./data/rtip.db
SECRET_KEY=your-super-secure-secret-key-change-this
API_KEY=your-api-access-key-for-external-access

# ===================
# Email Configuration  
# ===================
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password-or-password
ALERT_FROM_EMAIL=alerts@yourcompany.com
ALERT_TO_EMAIL=security@yourcompany.com

# ===================
# External API Keys (Optional)
# ===================
ABUSEIPDB_API_KEY=your-abuseipdb-api-key
VIRUSTOTAL_API_KEY=your-virustotal-api-key
SHODAN_API_KEY=your-shodan-api-key

# ===================
# AI Model Configuration
# ===================
ML_MODEL_PATH=./models/
ENABLE_GPU_ACCELERATION=false
AI_CONFIDENCE_THRESHOLD=0.8

# ===================
# Performance Settings
# ===================
MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT=30
CACHE_TTL=300
```

### 📧 Email Alert Setup

#### Gmail Configuration

1. **Enable 2-Factor Authentication**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password**
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Update Configuration**
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-gmail@gmail.com
   SMTP_PASSWORD=your-16-character-app-password
   ```

#### Microsoft Outlook Configuration

```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
```

#### Enterprise Email Configuration

```env
# Example for corporate email servers
SMTP_SERVER=mail.yourcompany.com
SMTP_PORT=587
SMTP_USERNAME=security@yourcompany.com
SMTP_PASSWORD=your-corporate-password
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### 🔐 Security Configuration

```env
# Strong secret keys (generate unique values)
SECRET_KEY=your-cryptographically-strong-secret-key-min-32-chars
JWT_SECRET_KEY=another-different-secret-key-for-jwt-tokens
API_KEY=secure-api-key-for-external-access

# Security settings
JWT_EXPIRY_MINUTES=60
API_RATE_LIMIT=1000
ENABLE_CORS=true
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### 🔌 API Keys Setup (Optional but Recommended)

#### AbuseIPDB API Key
1. Register at https://www.abuseipdb.com/register
2. Navigate to Account → API → Create Key
3. Add to `.env`: `ABUSEIPDB_API_KEY=your-key-here`

#### VirusTotal API Key  
1. Register at https://www.virustotal.com/gui/join-us
2. Go to your profile → API Key
3. Add to `.env`: `VIRUSTOTAL_API_KEY=your-key-here`

#### Shodan API Key
1. Register at https://www.shodan.io/
2. Navigate to Account → API Keys
3. Add to `.env`: `SHODAN_API_KEY=your-key-here`

---

## ✅ Post-Installation Verification

### 🌐 Access the Platform

#### Main Application Access
- 🖥️ **Web Dashboard**: http://localhost:3000
- 🔌 **API Documentation**: http://localhost:8000/docs
- ⚡ **Health Check**: http://localhost:8000/health

#### Expected Responses

**Dashboard (http://localhost:3000)**
- Should display the KRSN-RT2I dashboard
- Real-time threat statistics should be visible
- Navigation menu should be functional
- Dark/light theme toggle should work

**API Documentation (http://localhost:8000/docs)**
- Interactive Swagger UI should load
- Multiple endpoint categories should be visible:
  - Threat Detection APIs
  - Alert Management  
  - Dashboard Data
  - Health & Status

**Health Check (http://localhost:8000/health)**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-04T10:30:45.123Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "ai_models": "loaded",
    "cache": "connected"
  }
}
```

### 🧠 AI System Verification

#### Test Threat Detection API

```bash
# Test the threat detection endpoint
curl -X GET "http://localhost:8000/threat-detection/test-detection"

# Expected response:
{
  "is_threat": true,
  "confidence": 0.924,
  "severity": "HIGH", 
  "threat_type": "Network Anomaly",
  "timestamp": "2025-09-04T10:30:45",
  "processing_time_ms": 45,
  "model_version": "ensemble_v1.0"
}
```

#### Verify AI Model Status

```bash
# Check AI model status
curl -X GET "http://localhost:8000/threat-detection/model-status"

# Expected response:
{
  "models": {
    "random_forest": {
      "status": "loaded",
      "accuracy": 0.924,
      "last_updated": "2025-09-04T00:00:00"
    },
    "neural_network": {
      "status": "loaded", 
      "accuracy": 0.891,
      "last_updated": "2025-09-04T00:00:00"
    },
    "anomaly_detector": {
      "status": "loaded",
      "accuracy": 0.894,
      "last_updated": "2025-09-04T00:00:00"
    }
  },
  "ensemble_accuracy": 0.957
}
```

### 📊 Performance Verification

#### Response Time Testing

```bash
# Test API response times
for i in {1..10}; do
    echo "Request $i:"
    time curl -s -o /dev/null -w "Response Time: %{time_total}s\n" \
    "http://localhost:8000/threat-detection/test-detection"
done

# Expected: All responses under 100ms
```

#### Load Testing (Optional)

```bash
# Install Apache Bench (if needed)
# Ubuntu: sudo apt install apache2-utils
# macOS: brew install httpie

# Basic load test
ab -n 100 -c 10 http://localhost:8000/health

# Expected results:
# - 100% success rate
# - Average response time < 50ms
# - No failed requests
```

### 🔍 System Health Monitoring

#### Docker Container Status

```bash
# Check all containers are running
docker compose ps

# Expected output (all should show 'Up' status):
# NAME                        COMMAND              SERVICE   STATUS    PORTS
# krsn-backend-1             "uvicorn app.main:..." backend  Up (healthy) 0.0.0.0:8000->8000/tcp
# krsn-frontend-1            "nginx -g 'daemon o..." frontend Up (healthy) 0.0.0.0:3000->80/tcp
```

#### Resource Usage Check

```bash
# Monitor resource usage
docker stats --no-stream

# Expected resource usage:
# - CPU: < 30% under normal load
# - Memory: < 4GB total
# - Network I/O: Minimal when idle
```

#### Log Verification

```bash
# Check backend logs for errors
docker compose logs backend --tail=50

# Look for successful startup messages:
# ✅ Database connection established
# ✅ AI models loaded successfully
# ✅ Server started on port 8000

# Check frontend logs
docker compose logs frontend --tail=20

# Should show successful nginx startup
```

### 📧 Email System Testing

#### Send Test Alert

```bash
# Test email functionality via API
curl -X POST "http://localhost:8000/alerts/test-email" \
-H "Content-Type: application/json" \
-d '{
  "recipient": "your-email@example.com",
  "subject": "KRSN-RT2I Test Alert",
  "message": "This is a test alert from KRSN-RT2I"
}'

# Expected response:
{
  "status": "success",
  "message": "Test email sent successfully",
  "sent_at": "2025-09-04T10:30:45"
}
```

#### Verify Email Delivery

1. **Check your inbox** (and spam folder)
2. **Email should contain**:
   - Subject: "KRSN-RT2I Test Alert"
   - Sender matching your ALERT_FROM_EMAIL
   - Professional email template
   - Timestamp of alert

### 🎯 Dashboard Functionality Testing

#### Navigation Test
- ✅ Dashboard home page loads
- ✅ Threat analysis page accessible
- ✅ Alerts page functional
- ✅ Settings page available
- ✅ API documentation links work

#### Real-time Features
- ✅ Live threat counters update
- ✅ Recent alerts display
- ✅ System status indicators show green
- ✅ Charts and graphs render correctly

#### Interactive Elements
- ✅ Search functionality works
- ✅ Filters apply correctly
- ✅ Export functions operational
- ✅ Theme switching functional

---

## ⚙️ Advanced Configuration

### 🗄️ Database Configuration

#### PostgreSQL Setup (Production)

```bash
# Install PostgreSQL (Ubuntu/Debian)
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
postgres=# CREATE DATABASE krsn_rt2i;
postgres=# CREATE USER krsn_user WITH ENCRYPTED PASSWORD 'secure_password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE krsn_rt2i TO krsn_user;
postgres=# \q

# Update .env file
DATABASE_URL=postgresql://krsn_user:secure_password@localhost:5432/krsn_rt2i
```

#### Redis Setup (Caching)

```bash
# Install Redis (Ubuntu/Debian)
sudo apt install redis-server

# Start Redis service
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Update .env file
REDIS_URL=redis://localhost:6379
ENABLE_CACHING=true
```

### 🔒 Production Security Settings

#### SSL/TLS Configuration

```nginx
# nginx/ssl.conf
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/your/cert.pem;
    ssl_certificate_key /path/to/your/private.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    
    location / {
        proxy_pass http://frontend:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Environment Hardening

```env
# Production security settings
DEBUG=false
ENABLE_CORS=true
ALLOWED_ORIGINS=https://yourdomain.com
MAX_LOGIN_ATTEMPTS=5
SESSION_TIMEOUT=3600
ENABLE_2FA=true
PASSWORD_MIN_LENGTH=12
FORCE_HTTPS=true
```

### 📊 Monitoring & Logging

#### Prometheus Metrics

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'krsn-rt2i'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

#### Log Aggregation

```bash
# Configure log rotation
sudo tee /etc/logrotate.d/krsn-rt2i > /dev/null <<EOF
/var/log/krsn-rt2i/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 krsn krsn
}
EOF
```

### 🚀 Performance Optimization

#### Horizontal Scaling with Docker

```yaml
# docker-compose.prod.yml
version: '3.9'

services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  frontend:
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 1G

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    configs:
      - source: nginx_config
        target: /etc/nginx/nginx.conf
```

#### Kubernetes Deployment (Advanced)

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: krsn-rt2i-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: krsn-backend
  template:
    metadata:
      labels:
        app: krsn-backend
    spec:
      containers:
      - name: backend
        image: krsn/backend:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi" 
            cpu: "2"
```

---

## 🔧 Troubleshooting

### 🚨 Common Issues and Solutions

#### Issue 1: Docker Container Fails to Start

**Symptoms:**
```bash
Error: Cannot start container
Error: Port already in use
Container exits immediately
```

**Solutions:**

1. **Check Port Conflicts**
   ```bash
   # Windows
   netstat -an | findstr :3000
   netstat -an | findstr :8000
   
   # Linux/macOS  
   lsof -i :3000
   lsof -i :8000
   
   # Kill processes using the ports
   # Windows
   taskkill /PID <process_id> /F
   # Linux/macOS
   kill -9 <process_id>
   ```

2. **Check Docker Resources**
   ```bash
   # Clean up Docker resources
   docker system prune -a
   docker volume prune
   
   # Check available space
   docker system df
   ```

3. **Restart Docker Service**
   ```bash
   # Windows/macOS: Restart Docker Desktop
   # Linux:
   sudo systemctl restart docker
   ```

#### Issue 2: AI Models Not Loading

**Symptoms:**
```bash
Error: Model file not found
ImportError: Cannot import ML libraries
Model accuracy showing 0%
```

**Solutions:**

1. **Verify Model Files**
   ```bash
   # Check if model files exist
   ls -la models/
   
   # Expected files:
   # random_forest_threat_detector.pkl
   # neural_network_threat_detector.pkl  
   # anomaly_detector_threat_detector.pkl
   # scaler.pkl
   ```

2. **Reinstall Python Dependencies**
   ```bash
   pip install --force-reinstall scikit-learn joblib numpy pandas
   ```

3. **Retrain Models**
   ```bash
   python scripts/krsn_threat_detector.py --train
   ```

#### Issue 3: Frontend Build Errors

**Symptoms:**
```bash
ENOSPC: no space left on device
Module not found errors
Build process fails
```

**Solutions:**

1. **Clear Node.js Cache**
   ```bash
   npm cache clean --force
   # or
   pnpm store prune
   ```

2. **Increase Node Memory**
   ```bash
   # Add to package.json scripts:
   "dev": "NODE_OPTIONS='--max-old-space-size=4096' next dev"
   ```

3. **Check Disk Space**
   ```bash
   df -h  # Linux/macOS
   dir   # Windows
   ```

#### Issue 4: Database Connection Issues

**Symptoms:**
```bash
Database connection failed
Table does not exist
Permission denied accessing database
```

**Solutions:**

1. **Check Database File Permissions**
   ```bash
   # Create data directory with proper permissions
   mkdir -p backend/data
   chmod 755 backend/data
   
   # Check SQLite file
   ls -la backend/data/rtip.db
   ```

2. **Reset Database**
   ```bash
   # Backup existing data (if needed)
   cp backend/data/rtip.db backend/data/rtip_backup.db
   
   # Remove corrupted database
   rm backend/data/rtip.db
   
   # Restart services to recreate database
   docker compose down
   docker compose up -d
   ```

3. **Check Database URL**
   ```env
   # Ensure correct DATABASE_URL in .env
   DATABASE_URL=sqlite:///./data/rtip.db
   ```

#### Issue 5: Email Alerts Not Working

**Symptoms:**
```bash
SMTP authentication failed
Connection timeout
Emails not received
```

**Solutions:**

1. **Verify Email Configuration**
   ```bash
   # Test SMTP connection
   python -c "
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your-email@gmail.com', 'your-app-password')
   print('✅ SMTP connection successful')
   server.quit()
   "
   ```

2. **Check Gmail App Password**
   - Ensure 2FA is enabled
   - Use App Password (16 characters) not regular password
   - Allow "Less secure app access" if using regular password

3. **Test with Alternative SMTP**
   ```env
   # Try different SMTP settings
   SMTP_SERVER=smtp.office365.com  # For Outlook
   SMTP_PORT=587
   SMTP_USE_TLS=true
   ```

#### Issue 6: High Memory Usage

**Symptoms:**
```bash
Out of memory errors
System running slowly
Docker containers consuming too much RAM
```

**Solutions:**

1. **Limit Container Memory**
   ```yaml
   # Add to docker-compose.yml
   services:
     backend:
       deploy:
         resources:
           limits:
             memory: 2G
           reservations:
             memory: 1G
     frontend:
       deploy:
         resources:
           limits:
             memory: 512M
   ```

2. **Optimize Python Memory Usage**
   ```env
   # Add to .env
   PYTHONHASHSEED=1
   PYTHONUNBUFFERED=1
   PYTHONDONTWRITEBYTECODE=1
   ```

3. **Clean Up Docker**
   ```bash
   # Remove unused images and containers
   docker system prune -a
   docker image prune -a
   ```

### 📋 Diagnostic Commands

#### System Information Collection

```bash
#!/bin/bash
# diagnostic.sh - Collect system information for troubleshooting

echo "=== KRSN-RT2I System Diagnostic ==="
echo "Generated: $(date)"
echo

echo "=== System Information ==="
uname -a
echo "Docker Version: $(docker --version)"
echo "Docker Compose Version: $(docker compose version)"
echo

echo "=== Container Status ==="  
docker compose ps

echo "=== Container Resource Usage ==="
docker stats --no-stream

echo "=== Recent Logs (Backend) ==="
docker compose logs --tail=20 backend

echo "=== Recent Logs (Frontend) ==="
docker compose logs --tail=20 frontend

echo "=== Disk Usage ==="
df -h

echo "=== Memory Usage ==="
free -m

echo "=== Network Connectivity ==="
curl -I http://localhost:8000/health 2>/dev/null || echo "❌ Backend not accessible"
curl -I http://localhost:3000 2>/dev/null || echo "❌ Frontend not accessible"
```

#### Health Check Script

```bash
#!/bin/bash
# health-check.sh - Comprehensive health verification

echo "🔍 KRSN-RT2I Health Check"
echo "=========================="

# Check Docker services
echo "1. Checking Docker services..."
if docker compose ps | grep -q "Up"; then
    echo "✅ Docker services running"
else
    echo "❌ Docker services not running"
    exit 1
fi

# Check API health
echo "2. Checking API health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API healthy"
else
    echo "❌ Backend API not responding"
    exit 1
fi

# Check frontend
echo "3. Checking frontend..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend accessible"
else
    echo "❌ Frontend not accessible"
    exit 1
fi

# Check AI models
echo "4. Checking AI models..."
if curl -f http://localhost:8000/threat-detection/model-status > /dev/null 2>&1; then
    echo "✅ AI models loaded"
else
    echo "❌ AI models not loaded"
    exit 1
fi

echo
echo "🎉 All systems operational!"
```

### 🆘 Getting Help

#### Log Analysis

1. **Backend Logs**
   ```bash
   # View all backend logs
   docker compose logs backend
   
   # Follow live logs
   docker compose logs -f backend
   
   # Filter for errors only
   docker compose logs backend | grep -i error
   ```

2. **Frontend Logs**
   ```bash
   # View frontend logs
   docker compose logs frontend
   
   # Check nginx error logs
   docker compose exec frontend cat /var/log/nginx/error.log
   ```

#### Performance Monitoring

```bash
# Monitor system performance
watch -n 1 'docker stats --no-stream'

# Monitor API response times
while true; do
    start=$(date +%s%N)
    curl -s http://localhost:8000/health > /dev/null
    end=$(date +%s%N)
    echo "Response time: $((($end - $start) / 1000000)) ms"
    sleep 1
done
```

---

## 🔄 Maintenance & Updates

### 🔧 Regular Maintenance Tasks

#### Daily Tasks (Automated)
- ✅ Threat intelligence feed updates
- ✅ AI model inference and threat detection
- ✅ Log rotation and cleanup
- ✅ Database maintenance and optimization
- ✅ System health monitoring

#### Weekly Tasks

1. **System Health Review**
   ```bash
   # Check system performance
   ./health-check.sh
   
   # Review resource usage
   docker stats --no-stream
   
   # Check disk space
   df -h
   ```

2. **Update Threat Intelligence Feeds**
   ```bash
   # Manually trigger feed updates (if needed)
   curl -X POST "http://localhost:8000/feeds/update-all"
   ```

3. **Review Security Logs**
   ```bash
   # Check for security events
   docker compose logs backend | grep -i "security\|auth\|error"
   ```

#### Monthly Tasks

1. **Platform Updates**
   ```bash
   # Pull latest changes from repository
   git pull origin main
   
   # Rebuild containers with latest changes
   docker compose build --no-cache
   docker compose up -d
   ```

2. **Database Backup**
   ```bash
   # Create database backup
   mkdir -p backups
   docker compose exec backend cp /app/data/rtip.db /app/data/backup_$(date +%Y%m%d).db
   docker cp $(docker compose ps -q backend):/app/data/backup_$(date +%Y%m%d).db ./backups/
   ```

3. **AI Model Performance Review**
   ```bash
   # Get model performance metrics
   curl -X GET "http://localhost:8000/threat-detection/model-status"
   
   # Consider retraining if accuracy drops below 90%
   ```

4. **Security Updates**
   ```bash
   # Update base images
   docker compose pull
   docker compose up -d
   
   # Update Python dependencies
   pip install --upgrade -r backend/requirements.txt
   
   # Update Node.js dependencies
   npm update
   ```

### 📊 Backup and Recovery

#### Automated Backup Script

```bash
#!/bin/bash
# backup.sh - Automated backup script

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "🔄 Starting KRSN-RT2I backup..."

# Backup database
echo "📁 Backing up database..."
docker compose exec backend cp /app/data/rtip.db /app/data/backup.db
docker cp $(docker compose ps -q backend):/app/data/backup.db "$BACKUP_DIR/database.db"

# Backup configuration
echo "⚙️ Backing up configuration..."
cp .env "$BACKUP_DIR/env_backup"
cp docker-compose.yml "$BACKUP_DIR/compose_backup.yml"

# Backup trained models
echo "🧠 Backing up AI models..."
cp -r models/ "$BACKUP_DIR/models/"

# Backup logs (last 1000 lines)
echo "📝 Backing up logs..."
docker compose logs --tail=1000 > "$BACKUP_DIR/system_logs.txt"

# Create archive
echo "📦 Creating archive..."
tar -czf "backup_$(date +%Y%m%d_%H%M%S).tar.gz" -C backups/ "$(basename "$BACKUP_DIR")"

echo "✅ Backup completed: backup_$(date +%Y%m%d_%H%M%S).tar.gz"
```

#### Recovery Process

```bash
#!/bin/bash
# restore.sh - Recovery from backup

BACKUP_FILE=$1

if [[ -z "$BACKUP_FILE" ]]; then
    echo "Usage: ./restore.sh backup_YYYYMMDD_HHMMSS.tar.gz"
    exit 1
fi

echo "🔄 Starting KRSN-RT2I restoration..."

# Stop services
echo "⏹️ Stopping services..."
docker compose down

# Extract backup
echo "📦 Extracting backup..."
tar -xzf "$BACKUP_FILE"
BACKUP_DIR=$(tar -tzf "$BACKUP_FILE" | head -1 | cut -f1 -d"/")

# Restore database
echo "📁 Restoring database..."
cp "backups/$BACKUP_DIR/database.db" backend/data/rtip.db

# Restore configuration
echo "⚙️ Restoring configuration..."
cp "backups/$BACKUP_DIR/env_backup" .env
cp "backups/$BACKUP_DIR/compose_backup.yml" docker-compose.yml

# Restore models
echo "🧠 Restoring AI models..."
cp -r "backups/$BACKUP_DIR/models/"* models/

# Start services
echo "▶️ Starting services..."
docker compose up -d

echo "✅ Restoration completed successfully!"
```

### 🚀 Version Updates and Migrations

#### Update Process

```bash
#!/bin/bash
# update.sh - Safe update process

echo "🔄 KRSN-RT2I Update Process"
echo "============================"

# Create backup before update
echo "1. Creating backup..."
./backup.sh

# Pull latest changes
echo "2. Pulling latest changes..."
git fetch origin
git pull origin main

# Check for breaking changes
echo "3. Checking for migrations..."
if [[ -f "migrations/$(date +%Y%m).sql" ]]; then
    echo "⚠️ Database migrations required"
    echo "Please review migrations/$(date +%Y%m).sql"
    read -p "Continue with migration? (y/N): " confirm
    if [[ $confirm != "y" ]]; then
        echo "❌ Update cancelled"
        exit 1
    fi
fi

# Rebuild containers
echo "4. Rebuilding containers..."
docker compose build --no-cache

# Start with new version
echo "5. Starting updated version..."
docker compose up -d

# Verify health
echo "6. Verifying system health..."
sleep 30
./health-check.sh

echo "✅ Update completed successfully!"
```

### 📈 Performance Optimization

#### Monitoring Setup

```bash
# install-monitoring.sh - Set up monitoring stack

echo "📊 Setting up monitoring..."

# Create monitoring directory
mkdir -p monitoring/{prometheus,grafana}

# Create Prometheus config
cat > monitoring/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'krsn-rt2i'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
EOF

# Create Grafana dashboard
cat > monitoring/grafana/dashboard.json << EOF
{
  "dashboard": {
    "title": "KRSN-RT2I Monitoring",
    "panels": [
      {
        "title": "API Response Time",
        "type": "graph"
      },
      {
        "title": "Threat Detection Rate", 
        "type": "stat"
      }
    ]
  }
}
EOF

echo "✅ Monitoring setup complete"
echo "Access Grafana at: http://localhost:3001"
```

---

## 📖 Support & Documentation

### 📚 Documentation Resources

| Resource | Location | Description |
|----------|----------|-------------|
| **Main Documentation** | [README.md](../README.md) | Complete project overview and features |
| **API Reference** | [API_DOCS.md](API_DOCS.md) | Comprehensive API documentation |
| **System Architecture** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) | Technical architecture details |
| **Database Schema** | [ER_DIAGRAM.md](ER_DIAGRAM.md) | Database design and relationships |
| **AI Model Status** | [../AI_MODEL_STATUS.md](../AI_MODEL_STATUS.md) | AI system performance and status |
| **Live API Docs** | http://localhost:8000/docs | Interactive API documentation (when running) |

### 🤝 Community Support

#### GitHub Resources
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/STLR-TRAJ/GNN-POWERED-REAL-TIME-THREAT-CORRELATION/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/STLR-TRAJ/GNN-POWERED-REAL-TIME-THREAT-CORRELATION/discussions)
- 📚 **Documentation**: [Project Wiki](https://github.com/STLR-TRAJ/GNN-POWERED-REAL-TIME-THREAT-CORRELATION/wiki)

#### Response Times
- 🚨 **Critical Issues**: 24-48 hours
- 🐛 **Bug Reports**: 2-5 days  
- 💡 **Feature Requests**: 1-2 weeks
- 💬 **General Questions**: 3-7 days

### 👥 Development Team

**Project Lead & Architecture**
- 👨‍💻 **GitHub**: [@STLR-TRAJ](https://github.com/STLR-TRAJ)
- 🎯 **Role**: Full-stack development, AI/ML integration, system architecture
- 📧 **Academic Contact**: 2203051260006@PARULUNIVERSITY.AC.IN

**Academic Supervision**
- 🎓 **Institution**: PARUL INSTITUTE OF TECHNOLOGY, VADODARA
- 👨‍🏫 **Faculty Supervisor**: Prof. GAUTAM SINGH
- 🏛️ **University**: PARUL UNIVERSITY

### 🔍 Troubleshooting Resources

#### Quick Diagnostics

```bash
# Run comprehensive system check
curl -s https://raw.githubusercontent.com/STLR-TRAJ/GNN-POWERED-REAL-TIME-THREAT-CORRELATION/main/scripts/diagnostic.sh | bash

# Check specific component
python scripts/test_system.py --component backend
python scripts/test_system.py --component ai-models  
python scripts/test_system.py --component frontend
```

#### Common Issues Database

| Issue | Symptoms | Quick Fix |
|-------|----------|-----------|
| **Port Conflicts** | "Address already in use" | `./scripts/kill-ports.sh` |
| **AI Models Not Loading** | Zero accuracy, model errors | `python scripts/krsn_threat_detector.py --reload` |
| **Database Locked** | "Database is locked" | `docker compose restart backend` |
| **Memory Issues** | Container OOM killed | Add memory limits to docker-compose.yml |
| **Permission Denied** | File access errors | `sudo chown -R $USER:$USER .` |

### 📞 Professional Support

For enterprise deployments, custom integrations, or priority support:

- 📧 **Technical Support**: Available through GitHub Issues
- 🎓 **Academic Collaboration**: Contact university supervisors
- 🏢 **Enterprise Inquiries**: Create detailed issue with "enterprise" label
- 📝 **Consulting Services**: Available for complex deployments

### 🎯 Next Steps After Installation

1. **📊 Explore the Dashboard**
   - Navigate to http://localhost:3000
   - Familiarize yourself with the interface
   - Test threat detection features

2. **🔌 Try the APIs**  
   - Visit http://localhost:8000/docs
   - Test the threat detection endpoints
   - Integrate with your existing tools

3. **🧠 Understand the AI Models**
   - Review [AI_MODEL_STATUS.md](../AI_MODEL_STATUS.md)
   - Test with your own data
   - Consider custom model training

4. **🔒 Secure Your Installation**
   - Change default passwords
   - Configure SSL/TLS
   - Set up proper authentication

5. **📈 Monitor Performance**
   - Set up monitoring dashboards
   - Configure alerting
   - Establish backup procedures

---

## 🎉 Congratulations!

You have successfully installed and configured **KRSN-RT2I**, the advanced real-time threat intelligence platform! 

### 🛡️ What You Now Have:

- ✅ **Real-time AI-powered threat detection** with 95%+ accuracy
- ✅ **Modern web dashboard** with live threat visualization  
- ✅ **RESTful API endpoints** for seamless integration
- ✅ **Automated alerting system** for critical threats
- ✅ **Scalable architecture** ready for production deployment
- ✅ **Comprehensive documentation** and support resources

### 🚀 Ready to Secure Your Infrastructure

Your organization now has access to enterprise-grade cybersecurity intelligence capabilities. The KRSN-RT2I platform is actively monitoring for threats and ready to protect your digital assets.

### 🔗 Quick Access Links

- 🖥️ **Dashboard**: http://localhost:3000
- 🔌 **API Docs**: http://localhost:8000/docs  
- 📚 **Documentation**: [Project Wiki](https://github.com/STLR-TRAJ/GNN-POWERED-REAL-TIME-THREAT-CORRELATION/wiki)
- 🐛 **Support**: [GitHub Issues](https://github.com/STLR-TRAJ/GNN-POWERED-REAL-TIME-THREAT-CORRELATION/issues)

---

<div align="center">

### 🛡️ **Securing the Digital World with Intelligent Threat Detection**

**KRSN-RT2I** - *Advanced Real-Time Threat Intelligence Platform*

*Made with ❤️ for the cybersecurity community*

[![GitHub](https://img.shields.io/badge/GitHub-KRSN--RT2I-blue?style=for-the-badge&logo=github)](https://github.com/STLR-TRAJ/GNN-POWERED-REAL-TIME-THREAT-CORRELATION)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](../LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=for-the-badge)](http://localhost:8000/health)

</div>
