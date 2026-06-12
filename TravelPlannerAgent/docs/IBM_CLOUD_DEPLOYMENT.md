# 🚀 Deployment Guide - IBM Cloud Lite

**Travel Planner Agent - Production Deployment**

---

## Table of Contents
1. Prerequisites
2. Local Development Setup
3. IBM Cloud Lite Configuration
4. Deployment Steps
5. Post-Deployment Verification
6. Troubleshooting
7. Scaling & Monitoring

---

## Prerequisites

### System Requirements
- IBM Cloud account (Lite tier is free)
- IBM Cloud CLI installed
- Git installed
- Python 3.9+ installed
- 2GB+ available disk space

### Install IBM Cloud CLI
```bash
# Windows (PowerShell)
New-Item -ItemType Directory -Path "$env:ProgramFiles\IBM"
# Download installer from https://cloud.ibm.com/docs/cli

# For quick install on Mac/Linux
curl -fsSL https://clis.cloud.ibm.com/install/linux | bash

# Verify installation
ibmcloud --version
```

---

## Local Development Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/your-repo/TravelPlannerAgent.git
cd TravelPlannerAgent
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
# Add IBM Granite API key if available
# Add Weather API key if desired
```

### Step 5: Run Locally
```bash
python app.py
# Access: http://localhost:5000
```

### Step 6: Verify Installation
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test sample request
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "days": 3,
    "budget": 1500,
    "travel_type": "Couple",
    "interests": ["Food", "History"],
    "dietary_preferences": []
  }'
```

---

## IBM Cloud Lite Configuration

### Step 1: Create IBM Cloud Account
Log in to https://cloud.ibm.com and create a free Lite account

### Step 2: Create Resource Group
```bash
ibmcloud login --sso
ibmcloud account resource-groups

# Create if not exists
ibmcloud resource-group-create travel-planner-rg
```

### Step 3: Target Resource Group
```bash
ibmcloud target -g travel-planner-rg
```

### Step 4: Create Cloud Foundry Organization (if needed)
```bash
ibmcloud account orgs
# Note the org name or create new one
```

### Step 5: Set Org and Space
```bash
ibmcloud cf target -o YOUR_ORG -s development
# or create space
ibmcloud cf create-space development -o YOUR_ORG
```

---

## Deployment Steps

### Step 1: Prepare Manifest File

Create `manifest.yml` in project root:

```yaml
---
applications:
- name: travel-planner-agent
  instances: 1
  memory: 256M
  disk_quota: 512M
  command: python app.py
  buildpack: python_buildpack
  env:
    FLASK_APP: app.py
    FLASK_ENV: production
    FLASK_PORT: 8080
  memory: 256M
  routes:
  - route: travel-planner-agent.mybluemix.net
```

### Step 2: Update Requirements for Deployment

Ensure `Procfile` exists in root:

```
web: python app.py
```

Or update for Gunicorn:

```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

### Step 3: Prepare for Deployment

```bash
# Install Gunicorn locally for testing
pip install gunicorn
pip freeze > requirements.txt

# Test Gunicorn locally
gunicorn --bind 0.0.0.0:8080 app:app
```

### Step 4: Deploy to IBM Cloud

```bash
# Login to IBM Cloud
ibmcloud login --sso

# Target Cloud Foundry
ibmcloud target --cf

# Deploy application
ibmcloud cf push

# Monitor deployment
ibmcloud cf logs travel-planner-agent --recent
```

### Step 5: Verify Deployment

```bash
# Check app status
ibmcloud cf app travel-planner-agent

# View application details
ibmcloud cf apps

# Get app logs
ibmcloud cf logs travel-planner-agent --recent
```

---

## Post-Deployment Verification

### Test Health Endpoint
```bash
curl https://travel-planner-agent.mybluemix.net/api/health

# Expected Response:
# {
#   "status": "healthy",
#   "service": "Travel Planner Agent",
#   "timestamp": "2026-01-15T10:30:45"
# }
```

### Test Full Plan Generation
```bash
curl -X POST https://travel-planner-agent.mybluemix.net/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Tokyo",
    "days": 5,
    "budget": 3000,
    "travel_type": "Solo",
    "interests": ["Food", "Culture"],
    "dietary_preferences": []
  }'
```

### Check Application Logs
```bash
ibmcloud cf logs travel-planner-agent --recent --follow
```

### Monitor Performance
```bash
# View CPU and memory usage
ibmcloud cf stats travel-planner-agent

# View app events
ibmcloud cf events travel-planner-agent
```

---

## Environment Variables for Deployment

Set these in IBM Cloud:

```bash
# IBM Granite API Configuration
ibmcloud cf set-env travel-planner-agent IBM_API_KEY "your-api-key"
ibmcloud cf set-env travel-planner-agent IBM_WATSON_URL "https://api.us-south.watson-grove.ibm.com/instances/Your-Instance-ID"
ibmcloud cf set-env travel-planner-agent GRANITE_MODEL "ibm/granite-7b-instruct-v2"

# Weather API Configuration
ibmcloud cf set-env travel-planner-agent WEATHER_API_KEY "your-openweathermap-key"

# Application Configuration
ibmcloud cf set-env travel-planner-agent FLASK_ENV "production"
ibmcloud cf set-env travel-planner-agent SECRET_KEY "your-secret-key"

# Restage application
ibmcloud cf restage travel-planner-agent
```

---

## Scaling & Load Testing

### Scale Instances
```bash
# Increase instances to 3
ibmcloud cf scale travel-planner-agent -i 3

# Check current scaling
ibmcloud cf app travel-planner-agent
```

### Enable Auto-Scaling (requires paid plan)
```bash
# Create scaling policy
ibmcloud cf autoscaling-policy-create development travel-planner-agent \
  --min-instances 1 \
  --max-instances 5 \
  --metric cpu_percentage \
  --threshold 80
```

### Load Testing
```bash
# Using Apache Bench
ab -n 100 -c 10 https://travel-planner-agent.mybluemix.net/api/health

# Using curl in loop
for i in {1..50}; do
  curl https://travel-planner-agent.mybluemix.net/api/health &
done
```

---

## Troubleshooting

### Issue: "Application Failed to Start"
**Solution:**
```bash
# Check logs
ibmcloud cf logs travel-planner-agent --recent

# Common causes:
# 1. Port not 8080 (IBM Cloud expects this)
# 2. Python version mismatch
# 3. Missing dependencies

# Fix in code:
# app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

### Issue: "Out of Memory"
**Solution:**
```bash
# Increase memory allocation
ibmcloud cf scale travel-planner-agent -m 512M

# Monitor memory usage
ibmcloud cf stats travel-planner-agent
```

### Issue: "API Timeout"
**Solution:**
```bash
# Increase buildpack timeout
ibmcloud cf push --stack cflinuxfs4

# Add timeout to requests
# timeout=30 in requests.get() calls
```

### Issue: "Database Connection Failed"
**Solution:**
```bash
# Create database service
ibmcloud cf create-service cloudantnosqldb lite travel-db

# Bind to application
ibmcloud cf bind-service travel-planner-agent travel-db

# Access credentials
ibmcloud cf env travel-planner-agent | grep VCAP
```

### Issue: "Custom Domain Not Working"
**Solution:**
```bash
# Map custom domain
ibmcloud cf map-route travel-planner-agent example.com

# Verify DNS records point to IBM Cloud
# CNAME: travel-planner-agent.mybluemix.net
```

---

## Monitoring & Debugging

### Enable Debug Mode (Temporary Only)
```bash
ibmcloud cf set-env travel-planner-agent FLASK_DEBUG true
ibmcloud cf restage travel-planner-agent
```

### View Real-time Logs
```bash
ibmcloud cf logs travel-planner-agent --recent --follow
```

### Check Application Crashes
```bash
ibmcloud cf crash-report travel-planner-agent
```

### View Resource Usage
```bash
ibmcloud cf spaces
ibmcloud cf org-services travel-planner-rg
```

---

## Database Integration (IBM Cloudant)

### Step 1: Create Cloudant Service
```bash
ibmcloud cf create-service cloudantnosqldb lite travel-db
ibmcloud cf bind-service travel-planner-agent travel-db
```

### Step 2: Get Credentials
```bash
ibmcloud cf env travel-planner-agent | grep -A 20 travel-db
```

### Step 3: Update Application
```python
import os
import json
from cloudant.client import Cloudant

# Get credentials
vcap_services = json.loads(os.environ.get('VCAP_SERVICES', '{}'))
credentials = vcap_services['cloudantnosqldb'][0]['credentials']

# Initialize client
client = Cloudant(credentials['username'],
                 credentials['password'],
                 url=credentials['url'])
client.connect()

# Create database
db = client.create_database('travel-plans', throw_on_exists=False)
```

---

## CI/CD Pipeline Setup

### Using IBM DevOps
```bash
# Create toolchain
ibmcloud dev create-toolchain

# Configure Git repository
ibmcloud dev enable toolchain

# Deploy on push
ibmcloud cf enable-continuous-deployment
```

### Manual Pipeline
```bash
# Create .gitlab-ci.yml or .travis.yml
# Include build, test, deploy stages

stages:
  - build
  - test
  - deploy

deploy:
  script:
    - ibmcloud cf push
  only:
    - main
```

---

## Maintenance & Updates

### Update Dependencies
```bash
# Locally
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push

# Deploy
ibmcloud cf push
```

### Rollback Deployment
```bash
# List previous versions
ibmcloud cf revisions travel-planner-agent

# Rollback to previous
ibmcloud cf rollback travel-planner-agent
```

### Health Checks
```bash
# Set up health check endpoint
ibmcloud cf set-health-check travel-planner-agent http --endpoint /api/health

# Verify
ibmcloud cf app travel-planner-agent
```

---

## Billing & Quotas (Lite Plan)

### Lite Tier Limits
- **Instances**: Max 1
- **Memory**: 256MB total
- **Compute**: Small (0.25 vCPU)
- **Storage**: 512MB
- **API Calls**: Up to 100k/month
- **Cost**: Free

### Upgraded Plans
To scale beyond Lite:
```bash
# Switch to Standard plan
ibmcloud cf update-service travel-planner-agent -p standard

# Or create on paid tier during push
ibmcloud cf push --plan standard
```

---

## Disaster Recovery

### Backup Application
```bash
# Export application files
ibmcloud cf download travel-planner-agent

# Backup database
curl -X GET https://user:pass@account.cloudant.com/travel-plans
```

### Restore Application
```bash
# Push from backup
ibmcloud cf push --from-backup

# Or redeploy from git
git clone https://github.com/your-repo
cd TravelPlannerAgent
ibmcloud cf push
```

---

## Support & Resources

### IBM Cloud Documentation
- https://cloud.ibm.com/docs/cloud-foundry
- https://cloud.ibm.com/docs/watson

### IBM Granite LLM
- https://github.com/ibm-granite/granite-code-models
- https://cloud.ibm.com/docs/granite

### Flask Deployment
- https://flask.palletsprojects.com/en/2.3.x/deploying/
- https://gunicorn.org/

### Getting Help
- IBM Cloud Support: https://cloud.ibm.com/unifiedsupport
- GitHub Issues: [Your Repo Issues]
- Email: support@example.com

---

**Deployment Guide Version**: 1.0  
**Last Updated**: January 2026  
**Status**: Production Ready
