# 🚀 Setup Instructions - Travel Planner Agent

## System Requirements

### Minimum Requirements
- **Python**: 3.9 or higher
- **RAM**: 2GB (1GB minimum)
- **Disk**: 500MB free space
- **OS**: Windows, macOS, or Linux

### Software Requirements
- pip (Python package manager)
- Virtual environment (venv)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Step-by-Step Installation

### 1. Verify Python Installation

#### Windows
```powershell
python --version
pip --version
```

#### macOS/Linux
```bash
python3 --version
pip3 --version
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/)

### 2. Extract/Clone the Project

```bash
# Navigate to desired location
cd ~/Desktop

# Extract the TravelPlannerAgent folder
# OR clone from repository
git clone <repository-url>

cd TravelPlannerAgent
```

### 3. Create Virtual Environment

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

**Expected output:** `(venv)` prefix in terminal

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected:** All packages install without errors

### 5. Configure Environment (Optional)

Create a `.env` file in the project root:

```bash
# Windows PowerShell
cp .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=dev-secret-key-123

# IBM Granite Configuration (Optional)
IBM_API_KEY=your_api_key_here
IBM_WATSON_URL=https://api.us-south.mms.cloud.ibm.com/mms/v1
GRANITE_MODEL=granite-13b-chat-v2

# Weather API (Optional)
WEATHER_API_KEY=your_weather_api_key_here
```

### 6. Run the Application

```bash
python app.py
```

**Expected output:**
```
============================================================
🧳 Travel Planner Agent - Starting Server
============================================================
Environment: development
Debug Mode: True
Port: 5000
URL: http://localhost:5000
============================================================
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 7. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_ENV | Environment type | development |
| FLASK_PORT | Server port | 5000 |
| DEBUG | Debug mode | True |
| SECRET_KEY | Flask secret | auto-generated |
| IBM_API_KEY | Granite LLM key | empty |
| WEATHER_API_KEY | Weather API key | empty |

### Config Classes

Edit `config.py` to customize:

```python
class Config:
    AGENTS_TIMEOUT = 30  # seconds
    CACHE_TIMEOUT = 3600  # 1 hour
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

## IBM Cloud Integration (Optional)

### Setting Up IBM Granite API

1. **Create IBM Cloud Account**
   - Visit [ibm.com/cloud](https://www.ibm.com/cloud)
   - Sign up for free tier (Lite account)

2. **Create Watson service instance**
   - Go to Catalog
   - Search for "Watson Machine Learning"
   - Create service
   - Get API Key and URL

3. **Add to `.env`**
   ```env
   IBM_API_KEY=your_api_key_from_watson
   IBM_WATSON_URL=your_url_from_watson
   ```

4. **Test Integration**
   ```bash
   python -c "from services.granite_service import GraniteService; print(GraniteService().generate_text('Hello'))"
   ```

## Weather API Integration (Optional)

### Setting Up OpenWeatherMap API

1. **Register at OpenWeatherMap**
   - Visit [openweathermap.org](https://openweathermap.org)
   - Sign up for free account
   - Get API key from account settings

2. **Add to `.env`**
   ```env
   WEATHER_API_KEY=your_openweathermap_api_key
   ```

3. **Test Integration**
   ```bash
   python -c "from services.weather_service import WeatherService; print(WeatherService().get_current_weather('London'))"
   ```

## Running Tests

### Initialize Test Environment

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agents.py -v

# Run with coverage
pytest tests/ --cov=.
```

### Example Test Run

```bash
$ pytest tests/ -v

tests/test_agents.py::test_itinerary_agent PASSED
tests/test_agents.py::test_budget_agent PASSED
tests/test_services.py::test_granite_service PASSED
tests/test_api.py::test_health_endpoint PASSED

========================= 4 passed in 0.23s =========================
```

## Troubleshooting

### Issue 1: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

# Then install requirements
pip install -r requirements.txt
```

### Issue 2: Port Already in Use

**Error:**
```
OSError: [Errno 10048] Only one usage of each socket address
```

**Solution:**
```bash
# Use different port
set FLASK_PORT=5001
python app.py

# Or kill process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Issue 3: Python Not Found

**Error:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
- Install Python from [python.org](https://www.python.org)
- Add Python to PATH
- Use `python3` instead of `python` on macOS/Linux

### Issue 4: API Returns Empty Response

**Error:**
```
Empty response from granite service
```

**Solution:**
- Check IBM_API_KEY in `.env`
- Verify API key is valid in IBM Cloud console
- Check internet connection
- Fallback responses enabled by default

### Issue 5: Template Not Found

**Error:**
```
TemplateNotFound: index.html
```

**Solution:**
```bash
# Verify folder structure
# Ensure templates/index.html exists

# Check working directory
pwd
# Should be in TravelPlannerAgent folder

# Run from correct directory
cd TravelPlannerAgent
python app.py
```

## Production Deployment

### Requirements
- WSGI server (Gunicorn or uWSGI)
- Reverse proxy (Nginx)
- HTTPS/SSL certificate
- Database (PostgreSQL recommended)

### Deployment Steps

#### 1. Install Production Dependencies
```bash
pip install gunicorn psycopg2
```

#### 2. Update Configuration
```python
# config.py - Set to production
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
```

#### 3. Deploy with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### 4. Nginx Configuration
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### IBM Cloud Dervoyment

#### Using IBM Cloud CLI

1. Install IBM Cloud CLI
2. Login to IBM Cloud
   ```bash
   ibmcloud login
   ```
3. Deploy
   ```bash
   ibmcloud cf push TravelPlannerAgent
   ```

#### Using Docker

```bash
# Create Dockerfile
docker build -t travel-planner:latest .

# Run container
docker run -p 5000:5000 travel-planner:latest
```

## Common Commands

### Activation/Deactivation

```bash
# Activate virtual environment
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

# Deactivate virtual environment
deactivate
```

### Running Server

```bash
# Development
python app.py

# Production
gunicorn -w 4 app:app

# Different port
FLASK_PORT=5001 python app.py
```

### Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_agents.py::test_itinerary_agent

# With coverage
pytest --cov

# Verbose mode
pytest -v
```

### Package Management

```bash
# Install new package
pip install package-name

# List installed packages
pip list

# Freeze dependencies
pip freeze > requirements.txt

# Uninstall package
pip uninstall package-name
```

## File Permissions

### macOS/Linux

```bash
# Make script executable
chmod +x app.py

# Make directory readable
chmod 755 templates/
chmod 755 static/
```

## Getting Help

### Resources
1. **Flask Documentation**: [flask.palletsprojects.com](https://flask.palletsprojects.com)
2. **Python Documentation**: [python.org/doc](https://docs.python.org)
3. **IBM Cloud Documentation**: [cloud.ibm.com/docs](https://cloud.ibm.com/docs)

### Community Support
- Stack Overflow with tags: `flask`, `python`, `ibm-cloud`
- GitHub Issues on project repository
- IBM Cloud Support Portal

### Debugging

Enable verbose logging:

```python
# In app.py
import logging

logging.basicConfig(level=logging.DEBUG)
```

---

**Setup Guide v1.0** | Travel Planner Agent
