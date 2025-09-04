# 🚀 RTIP Platform Installation Guide

**Real-time Threat Intelligence Platform for SMEs**

This comprehensive guide will walk you through installing and configuring the RTIP Platform on your system. The guide is designed for both technical and non-technical users.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installing Docker](#installing-docker)
4. [Downloading the RTIP Platform](#downloading-the-rtip-platform)
5. [Configuration](#configuration)
6. [Installation](#installation)
7. [Post-Installation Verification](#post-installation-verification)
8. [Email Configuration](#email-configuration)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance](#maintenance)
11. [Support](#support)

---

## 🔧 Prerequisites

Before installing the RTIP Platform, ensure you have:

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+, CentOS 7+)
- **Internet Connection**: Required for downloading components and threat feeds
- **Administrator/Root Access**: Needed for Docker installation
- **Email Account**: For receiving threat alerts (Gmail, Outlook, or corporate email)

---

## 💻 System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 10 GB free space
- **Network**: Broadband internet connection

### Recommended Requirements
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Storage**: 20 GB free space (SSD preferred)
- **Network**: Stable broadband connection

---

## 🐳 Installing Docker

Docker is required to run the RTIP Platform. Follow the instructions for your operating system:

### Windows Installation

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"
   - Run the installer as Administrator

2. **Install Docker Desktop**
   - Double-click the downloaded file
   - Follow the installation wizard
   - Restart your computer when prompted

3. **Verify Installation**
   - Open Command Prompt or PowerShell
   - Run: `docker --version`
   - You should see version information

### macOS Installation

1. **Download Docker Desktop**
   - Visit: https://www.docker.com/products/docker-desktop
   - Click "Download for Mac"
   - Choose the appropriate version (Intel or Apple Silicon)

2. **Install Docker Desktop**
   - Open the downloaded .dmg file
   - Drag Docker to Applications folder
   - Launch Docker from Applications

3. **Verify Installation**
   - Open Terminal
   - Run: `docker --version`
   - You should see version information

### Linux Installation (Ubuntu/Debian)

1. **Update Package Index**
   \`\`\`bash
   sudo apt update
   \`\`\`

2. **Install Prerequisites**
   \`\`\`bash
   sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release
   \`\`\`

3. **Add Docker's Official GPG Key**
   \`\`\`bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   \`\`\`

4. **Add Docker Repository**
   \`\`\`bash
   echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   \`\`\`

5. **Install Docker**
   \`\`\`bash
   sudo apt update
   sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
   \`\`\`

6. **Start Docker Service**
   \`\`\`bash
   sudo systemctl start docker
   sudo systemctl enable docker
   \`\`\`

7. **Add User to Docker Group** (Optional)
   \`\`\`bash
   sudo usermod -aG docker $USER
   \`\`\`
   Log out and back in for changes to take effect.

8. **Verify Installation**
   \`\`\`bash
   docker --version
   docker compose version
   \`\`\`

---

## 📥 Downloading the RTIP Platform

### Method 1: Using Git (Recommended)

1. **Install Git** (if not already installed)
   - **Windows**: Download from https://git-scm.com/download/win
   - **macOS**: Install via Homebrew: `brew install git`
   - **Linux**: `sudo apt install git` (Ubuntu/Debian)

2. **Clone the Repository**
   \`\`\`bash
   git clone https://github.com/your-organization/rtip-platform.git
   cd rtip-platform
   \`\`\`

### Method 2: Download ZIP File

1. **Download the ZIP**
   - Visit the GitHub repository
   - Click "Code" → "Download ZIP"
   - Extract the ZIP file to your desired location

2. **Navigate to Directory**
   \`\`\`bash
   cd rtip-platform
   \`\`\`

---

## ⚙️ Configuration

### 1. Environment Variables Setup

1. **Copy the Example Configuration**
   \`\`\`bash
   cp .env.example .env
   \`\`\`

2. **Edit the Configuration File**
   
   **Windows**: Use Notepad or any text editor
   \`\`\`cmd
   notepad .env
   \`\`\`
   
   **macOS/Linux**: Use nano, vim, or any text editor
   \`\`\`bash
   nano .env
   \`\`\`

3. **Configure Required Settings**

   \`\`\`env
   # Database Configuration (Leave as default for SQLite)
   DATABASE_URL=sqlite:///./data/rtip.db

   # Email Alert Configuration (REQUIRED)
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ALERT_FROM_EMAIL=alerts@yourcompany.com
   ALERT_TO_EMAIL=security@yourcompany.com

   # Security Configuration (CHANGE THESE!)
   SECRET_KEY=your-very-secure-secret-key-here-change-this
   API_KEY=your-api-access-key-for-external-access

   # External API Keys (Optional but recommended)
   ABUSEIPDB_API_KEY=your-abuseipdb-api-key
   VIRUSTOTAL_API_KEY=your-virustotal-api-key
   \`\`\`

### 2. Email Configuration Guide

#### Gmail Setup

1. **Enable 2-Factor Authentication**
   - Go to Google Account settings
   - Security → 2-Step Verification → Turn On

2. **Generate App Password**
   - Security → 2-Step Verification → App passwords
   - Select "Mail" and your device
   - Copy the generated 16-character password

3. **Update .env File**
   \`\`\`env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-gmail@gmail.com
   SMTP_PASSWORD=your-16-character-app-password
   \`\`\`

#### Outlook/Hotmail Setup

\`\`\`env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
\`\`\`

#### Corporate Email Setup

Contact your IT administrator for:
- SMTP server address
- Port number (usually 587 or 25)
- Authentication requirements

### 3. API Keys Configuration (Optional)

#### AbuseIPDB API Key

1. **Register at AbuseIPDB**
   - Visit: https://www.abuseipdb.com/register
   - Create a free account
   - Go to Account → API → Create Key

2. **Add to .env File**
   \`\`\`env
   ABUSEIPDB_API_KEY=your-abuseipdb-key-here
   \`\`\`

#### VirusTotal API Key

1. **Register at VirusTotal**
   - Visit: https://www.virustotal.com/gui/join-us
   - Create a free account
   - Go to Profile → API Key

2. **Add to .env File**
   \`\`\`env
   VIRUSTOTAL_API_KEY=your-virustotal-key-here
   \`\`\`

---

## 🚀 Installation

### 1. Build and Start the Platform

\`\`\`bash
# Build and start all services
docker compose up -d
\`\`\`

This command will:
- Download required Docker images
- Build the application containers
- Start the database, backend, and frontend services
- Set up networking between components

### 2. Monitor Installation Progress

\`\`\`bash
# View logs to monitor progress
docker compose logs -f
\`\`\`

Press `Ctrl+C` to stop viewing logs (services continue running).

### 3. Check Service Status

\`\`\`bash
# Check if all services are running
docker compose ps
\`\`\`

You should see three services running:
- `rtip-platform-backend-1`
- `rtip-platform-frontend-1`
- `rtip-platform-nginx-1` (if using production profile)

---

## ✅ Post-Installation Verification

### 1. Access the Platform

1. **Open Web Browser**
   - Navigate to: http://localhost:3000
   - You should see the RTIP Platform dashboard

2. **Check API Documentation**
   - Navigate to: http://localhost:8000/docs
   - You should see the interactive API documentation

### 2. Verify System Health

1. **Dashboard Health Check**
   - On the dashboard, look for the system status indicator
   - Should show "System Healthy" with green indicator

2. **API Health Check**
   - Visit: http://localhost:8000/health
   - Should return: `{"status": "healthy"}`

### 3. Test Email Alerts

1. **Send Test Alert**
   - In the dashboard, look for "Send Test Alert" button
   - Click to send a test email
   - Check your configured email address

2. **Verify Email Reception**
   - Check inbox (and spam folder)
   - Should receive "RTIP Threat Alert" test email

### 4. Verify Threat Feed Ingestion

1. **Check Dashboard Metrics**
   - Total threats should be > 0 after 5-10 minutes
   - Recent threats should show activity

2. **Browse Threats**
   - Navigate to "Threats" section
   - Should see threat indicators from various sources

---

## 📧 Email Configuration

### Setting Up Multiple Recipients

1. **Edit Alert Configuration**
   \`\`\`env
   ALERT_TO_EMAIL=security@company.com,admin@company.com,soc@company.com
   \`\`\`

2. **Configure Alert Thresholds**
   \`\`\`env
   # Only send alerts for High and Critical threats
   ALERT_SEVERITY_THRESHOLD=High
   
   # Limit alerts to prevent spam
   ALERT_RATE_LIMIT_PER_HOUR=5
   \`\`\`

### Custom Email Templates

1. **Access Alert Configuration API**
   - Navigate to: http://localhost:8000/docs
   - Look for `/api/v1/alerts/configurations` endpoints

2. **Create Custom Configuration**
   \`\`\`bash
   curl -X POST "http://localhost:8000/api/v1/alerts/configurations" \
   -H "Authorization: Bearer your-api-key" \
   -H "Content-Type: application/json" \
   -d '{
     "config_name": "custom_alerts",
     "email_enabled": true,
     "email_recipients": ["security@company.com"],
     "severity_threshold": "High",
     "max_alerts_per_hour": 10
   }'
   \`\`\`

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Docker Not Starting

**Symptoms:**
- Error: "Docker daemon not running"
- Cannot execute docker commands

**Solutions:**
1. **Windows/macOS**: Start Docker Desktop application
2. **Linux**: Start Docker service
   \`\`\`bash
   sudo systemctl start docker
   \`\`\`

#### Issue 2: Port Already in Use

**Symptoms:**
- Error: "Port 3000 is already allocated"
- Error: "Port 8000 is already allocated"

**Solutions:**
1. **Stop conflicting services:**
   \`\`\`bash
   # Find processes using the ports
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :8000
   
   # Kill the processes (replace PID with actual process ID)
   kill -9 PID
   \`\`\`

2. **Change ports in docker-compose.yml:**
   \`\`\`yaml
   services:
     frontend:
       ports:
         - "3001:80"  # Change from 3000 to 3001
     backend:
       ports:
         - "8001:8000"  # Change from 8000 to 8001
   \`\`\`

#### Issue 3: Email Alerts Not Working

**Symptoms:**
- Test alerts not received
- Email authentication errors

**Solutions:**
1. **Check email credentials:**
   - Verify SMTP settings in .env file
   - Ensure app password is correct (for Gmail)

2. **Check firewall/antivirus:**
   - Temporarily disable to test
   - Add Docker to exceptions

3. **Test SMTP connection:**
   \`\`\`bash
   # Access backend container
   docker compose exec backend python -c "
   import smtplib
   server = smtplib.SMTP('smtp.gmail.com', 587)
   server.starttls()
   server.login('your-email@gmail.com', 'your-app-password')
   print('SMTP connection successful')
   server.quit()
   "
   \`\`\`

#### Issue 4: Database Errors

**Symptoms:**
- "Database connection failed"
- "Table doesn't exist" errors

**Solutions:**
1. **Reset database:**
   \`\`\`bash
   # Stop services
   docker compose down
   
   # Remove database volume
   docker volume rm rtip-platform_data
   
   # Restart services
   docker compose up -d
   \`\`\`

2. **Check database permissions:**
   \`\`\`bash
   # Ensure data directory exists and is writable
   mkdir -p data
   chmod 755 data
   \`\`\`

#### Issue 5: Threat Feeds Not Updating

**Symptoms:**
- No threats in dashboard
- Feed status shows errors

**Solutions:**
1. **Check internet connectivity:**
   \`\`\`bash
   # Test from container
   docker compose exec backend curl -I https://api.abuseipdb.com
   \`\`\`

2. **Verify API keys:**
   - Check .env file for correct API keys
   - Test API keys on respective websites

3. **Check logs:**
   \`\`\`bash
   docker compose logs backend | grep -i "feed\|ingest"
   \`\`\`

#### Issue 6: High Memory Usage

**Symptoms:**
- System running slowly
- Docker containers consuming too much memory

**Solutions:**
1. **Limit container memory:**
   \`\`\`yaml
   # Add to docker-compose.yml services
   services:
     backend:
       deploy:
         resources:
           limits:
             memory: 1G
     frontend:
       deploy:
         resources:
           limits:
             memory: 512M
   \`\`\`

2. **Clean up Docker:**
   \`\`\`bash
   # Remove unused containers and images
   docker system prune -a
   \`\`\`

### Log Analysis

#### Viewing Logs

\`\`\`bash
# View all logs
docker compose logs

# View specific service logs
docker compose logs backend
docker compose logs frontend

# Follow logs in real-time
docker compose logs -f

# View last 100 lines
docker compose logs --tail=100
\`\`\`

#### Common Log Messages

**Normal Operation:**
\`\`\`
✅ Database tables created/verified
✅ Initial threat feed ingestion completed
🎯 RTIP Platform started successfully!
\`\`\`

**Warning Messages:**
\`\`\`
⚠️ AbuseIPDB API key not configured, skipping
⚠️ Rate limit exceeded for configuration 'default'
\`\`\`

**Error Messages:**
\`\`\`
❌ Error fetching from AbuseIPDB: HTTP 401 Unauthorized
❌ Failed to send email alert: Authentication failed
\`\`\`

---

## 🔄 Maintenance

### Regular Maintenance Tasks

#### Daily Tasks (Automated)
- Threat feed ingestion
- Database cleanup
- Log rotation

#### Weekly Tasks
1. **Check System Health**
   \`\`\`bash
   # View system status
   docker compose ps
   docker stats
   \`\`\`

2. **Review Alert Logs**
   - Check dashboard for alert statistics
   - Verify email delivery rates

#### Monthly Tasks
1. **Update Platform**
   \`\`\`bash
   # Pull latest changes
   git pull origin main
   
   # Rebuild containers
   docker compose build --no-cache
   docker compose up -d
   \`\`\`

2. **Database Maintenance**
   \`\`\`bash
   # Backup database
   docker compose exec backend sqlite3 /app/data/rtip.db ".backup /app/data/backup_$(date +%Y%m%d).db"
   \`\`\`

3. **Clean Up Old Data**
   \`\`\`bash
   # Remove old logs and temporary files
   docker compose exec backend find /app/data -name "*.log" -mtime +30 -delete
   \`\`\`

### Backup and Recovery

#### Creating Backups

1. **Database Backup**
   \`\`\`bash
   # Create backup directory
   mkdir -p backups
   
   # Backup database
   docker compose exec backend sqlite3 /app/data/rtip.db ".backup /app/data/backup.db"
   docker cp $(docker compose ps -q backend):/app/data/backup.db ./backups/rtip_backup_$(date +%Y%m%d).db
   \`\`\`

2. **Configuration Backup**
   \`\`\`bash
   # Backup configuration files
   cp .env backups/env_backup_$(date +%Y%m%d)
   cp docker-compose.yml backups/compose_backup_$(date +%Y%m%d).yml
   \`\`\`

#### Restoring from Backup

1. **Stop Services**
   \`\`\`bash
   docker compose down
   \`\`\`

2. **Restore Database**
   \`\`\`bash
   # Copy backup to data directory
   cp backups/rtip_backup_YYYYMMDD.db data/rtip.db
   \`\`\`

3. **Restart Services**
   \`\`\`bash
   docker compose up -d
   \`\`\`

### Performance Optimization

#### Database Optimization

1. **Enable WAL Mode** (for better performance)
   \`\`\`bash
   docker compose exec backend sqlite3 /app/data/rtip.db "PRAGMA journal_mode=WAL;"
   \`\`\`

2. **Analyze Database**
   \`\`\`bash
   docker compose exec backend sqlite3 /app/data/rtip.db "ANALYZE;"
   \`\`\`

#### Resource Monitoring

\`\`\`bash
# Monitor resource usage
docker stats

# Check disk usage
docker compose exec backend df -h

# Monitor database size
docker compose exec backend ls -lh /app/data/
\`\`\`

---

## 🆘 Support

### Getting Help

#### Documentation
- **API Documentation**: http://localhost:8000/docs
- **GitHub Repository**: https://github.com/your-organization/rtip-platform
- **Wiki**: https://github.com/your-organization/rtip-platform/wiki

#### Community Support
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share experiences
- **Discord/Slack**: Real-time community support

#### Professional Support
- **Email**: support@rtip-platform.org
- **Commercial Support**: Available for enterprise deployments

### Reporting Issues

When reporting issues, please include:

1. **System Information**
   \`\`\`bash
   # Gather system info
   echo "OS: $(uname -a)"
   echo "Docker: $(docker --version)"
   echo "Docker Compose: $(docker compose version)"
   \`\`\`

2. **Service Status**
   \`\`\`bash
   docker compose ps
   docker compose logs --tail=50
   \`\`\`

3. **Configuration** (remove sensitive data)
   \`\`\`bash
   # Sanitized environment variables
   cat .env | grep -v PASSWORD | grep -v KEY
   \`\`\`

4. **Error Messages**
   - Copy exact error messages
   - Include relevant log entries
   - Describe steps to reproduce

### Frequently Asked Questions

#### Q: Can I run RTIP on a different port?
**A:** Yes, modify the ports in `docker-compose.yml`:
\`\`\`yaml
services:
  frontend:
    ports:
      - "8080:80"  # Change from 3000 to 8080
\`\`\`

#### Q: How do I add more threat intelligence sources?
**A:** Edit `backend/app/services/feed_ingestor.py` and add new feed methods to the `feeds` dictionary.

#### Q: Can I use PostgreSQL instead of SQLite?
**A:** Yes, update the `DATABASE_URL` in `.env`:
\`\`\`env
DATABASE_URL=postgresql://user:password@localhost:5432/rtip
\`\`\`

#### Q: How do I configure HTTPS?
**A:** Use a reverse proxy like nginx or Traefik with SSL certificates. Example nginx configuration is provided in the repository.

#### Q: Can I customize the dashboard?
**A:** Yes, the frontend is built with Vue.js. Modify files in `frontend/src/` and rebuild the containers.

---

## 🎉 Congratulations!

You have successfully installed and configured the RTIP Platform! Your organization now has:

- ✅ **Real-time threat intelligence** from multiple sources
- ✅ **Automated email alerts** for critical threats
- ✅ **User-friendly dashboard** for threat monitoring
- ✅ **Search capabilities** for threat investigation
- ✅ **API access** for integration with other tools

### Next Steps

1. **Customize Alert Settings**
   - Configure recipient lists
   - Set severity thresholds
   - Create custom alert templates

2. **Integrate with Existing Tools**
   - Use the API to feed data to SIEM systems
   - Set up webhook notifications
   - Export threat data for analysis

3. **Train Your Team**
   - Familiarize staff with the dashboard
   - Establish incident response procedures
   - Create documentation for your organization

4. **Monitor and Maintain**
   - Review alerts regularly
   - Keep the platform updated
   - Monitor system performance

### Stay Secure! 🛡️

The RTIP Platform is now protecting your organization with real-time threat intelligence. Remember to:
- Review alerts promptly
- Keep your systems updated
- Maintain good cybersecurity practices
- Share threat intelligence with the community

---

**Need help?** Contact our support team or visit the community forums.

**Happy threat hunting!** 🕵️‍♂️
