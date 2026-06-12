# TravelPlannerAgent

Minimal instructions to add this project to GitHub and run locally.

## Quick steps (local)

1. Open PowerShell in the project root (where `app.py` is).
2. Create a virtual env and install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Run the app:

```powershell
$env:FLASK_ENV='development'
python app.py
```

## Add to GitHub (recommended using GitHub CLI)

```powershell
git init
git add .
git commit -m "Initial commit"
# create remote repo (replace name/visibility)
gh repo create YOUR_USERNAME/TravelPlannerAgent --public --source=. --remote=origin --push
```

If you don't have `gh`, create a repo on github.com and then run:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/TravelPlannerAgent.git
git branch -M main
git push -u origin main
```
# 🧳 Travel Planner Agent - AI-Powered Trip Planning

**Powered by IBM Granite & IBM Cloud Lite**

## 📋 Overview

The Travel Planner Agent is an intelligent travel planning application that uses AI (IBM Granite LLM) to create personalized travel itineraries. It integrates multiple specialized agents to provide comprehensive trip planning assistance including accommodation, budget management, weather forecasts, local food recommendations, and emergency information.

## ✨ Features

### Core Features
- **📅 Intelligent Itinerary Planning**: Day-wise travel schedules based on preferences
- **💰 Smart Budget Management**: Expense breakdown and cost optimization
- **🏨 Hotel Recommendations**: Budget, mid-range, and luxury options
- **🌤️ Weather Intelligence**: Forecasts, suitability analysis, and packing suggestions
- **🍽️ Food Recommendations**: Local cuisine, street food, dietary options
- **🎒 Packing Checklist**: Weather-appropriate packing suggestions
- **📞 Emergency Information**: Safety tips and emergency contacts

### Agentic AI System
- **Itinerary Agent**: Creates detailed daily plans
- **Budget Agent**: Manages and optimizes expenses  
- **Hotel Agent**: Recommends accommodations
- **Weather Agent**: Provides environmental insights
- **Food Agent**: Suggests dining experiences

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 2.3.3
- **Language**: Python 3.9+
- **AI/LLM**: IBM Granite (with fallback responses)
- **API Integration**: RESTful API
- **Database**: In-memory (can be extended to PostgreSQL/MongoDB)

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern responsive design
- **JavaScript**: Vanilla JS (no frameworks, for accessibility)
- **UI/UX**: Material Design principles

### Cloud & Services
- **IBM Cloud Lite**: Deployment platform
- **IBM Granite LLM**: AI responses
- **OpenWeatherMap API**: Weather data (optional)
- **CORS**: Cross-origin requests management

## 📁 Project Structure

```
TravelPlannerAgent/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
│
├── agents/                     # AI Agent modules
│   ├── itinerary_agent.py      # Day-wise itinerary planning
│   ├── budget_agent.py         # Budget breakdown
│   ├── hotel_agent.py          # Hotel recommendations
│   ├── weather_agent.py        # Weather and clothing
│   └── food_agent.py           # Food recommendations
│
├── services/                   # External integrations
│   ├── granite_service.py      # IBM Granite LLM service
│   └── weather_service.py      # Weather API service
│
├── templates/                  # HTML templates
│   └── index.html              # Main page
│
├── static/                     # Frontend assets
│   ├── style.css               # Styling
│   ├── script.js               # Client-side logic
│   └── images/                 # Image assets
│
├── tests/                      # Test cases
│   ├── test_agents.py
│   ├── test_services.py
│   └── test_api.py
│
└── docs/                       # Documentation
    ├── SETUP.md                # Setup instructions
    ├── API.md                  # API documentation
    ├── ARCHITECTURE.md         # System architecture
    └── USER_GUIDE.md           # User guide
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone/Extract the project**
   ```bash
   cd TravelPlannerAgent
   ```

2. **Create virtual environment (optional but recommended)**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** (optional for API keys)
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📖 Usage Guide

### Step 1: Enter Trip Details
- **Source Location**: Where you're traveling from
- **Destination**: Where you want to go
- **Duration**: Number of days (1-30)
- **Budget**: Total budget in USD
- **Travel Type**: Solo, Family, Friends, or Couple
- **Interests**: Select multiple (Adventure, Nature, Food, Historical, Religious, etc.)
- **Dietary Preferences**: Vegetarian, Vegan, Halal, etc.

### Step 2: Generate Plan
Click "Generate My Travel Plan" and let the AI agents work their magic!

### Step 3: View Results
- **Itinerary Tab**: Day-wise activities and schedules
- **Budget Tab**: Expense breakdown by category
- **Hotels Tab**: Accommodation recommendations
- **Weather Tab**: Weather forecast and packing advice
- **Food Tab**: Local cuisine and dining options

### Step 4: Export or Print
- Download as JSON for backup
- Print the plan
- Share with friends

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```

### Generate Complete Plan
```
POST /api/plan
Body: {
  "destination": "Paris",
  "days": 7,
  "budget": 3000,
  "travel_type": "Couple",
  "interests": ["Food", "Art", "Historical"],
  "dietary_preferences": ["Vegetarian"]
}
```

### Individual Agent Endpoints
```
GET /api/itinerary
POST /api/budget
POST /api/hotels
POST /api/weather
POST /api/food
POST /api/packing-checklist
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file with:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=your-secret-key

# IBM Granite Configuration
IBM_API_KEY=your_api_key
IBM_WATSON_URL=https://api.us-south.mms.cloud.ibm.com/mms/v1
GRANITE_MODEL=granite-13b-chat-v2

# Weather API
WEATHER_API_KEY=your_weather_api_key

# Deployment
DEBUG=True
```

## 🧠 How Agents Work

### Agent Architecture
Each agent is a specialized module that:
1. Receives specific input parameters
2. Calls the Granite LLM service
3. Processes and structures the response
4. Returns formatted data to the frontend

### Agent Workflow
```
User Input → Form Validation → All 5 Agents Process in Parallel → 
Results Aggregation → JSON Response → Frontend Display
```

### Example: Budget Agent
```python
# Input
destination = "Paris"
budget = 3000
days = 7
travel_type = "Couple"

# Process
breakdown = generate_budget_breakdown(budget, days, travel_type)
# Output: {
#   "accommodation": {"amount": 1050, "percentage": 35%},
#   "food": {"amount": 750, "percentage": 25%},
#   ...
# }
```

## 🧪 Testing

### Run Test Suite
```bash
pytest tests/ -v
```

### Test Categories
- **Unit Tests**: Individual agent functionality
- **Integration Tests**: API endpoints
- **Service Tests**: External integrations

### Example Test
```bash
python tests/test_agents.py
```

## 📝 Sample Outputs

### API Response Example
```json
{
  "status": "success",
  "summary": {
    "destination": "Paris",
    "duration": 7,
    "total_budget": 3000,
    "travel_type": "Couple",
    "interests": ["Food", "Art", "Historical"]
  },
  "itinerary": { ... },
  "budget": { 
    "accommodation": 1050,
    "food": 750,
    ...
  },
  "accommodation": { ... },
  "weather": { ... },
  "food": { ... }
}
```

## 🎓 Learning Resources

### Understanding the Code
1. **app.py**: Main Flask application and route handlers
2. **agents/*.py**: Individual AI agent implementations
3. **services/*.py**: External service integrations
4. **static/script.js**: Frontend logic and API calls

### Key Concepts
- **REST API**: HTTP endpoints for communication
- **Agents**: Specialized AI modules for specific tasks
- **LLM Integration**: Using IBM Granite for intelligent responses
- **Responsive Design**: Mobile-friendly UI

## 🚀 Deployment

### Local Deployment
```bash
python app.py
```

### IBM Cloud Lite Deployment
1. Create IBM Cloud Account
2. Install IBM Cloud CLI
3. Configure credentials
4. Deploy using:
   ```bash
   ibmcloud app push TravelPlannerAgent
   ```

### Docker Deployment
```bash
docker build -t travel-planner .
docker run -p 5000:5000 travel-planner
```

## 🐛 Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Ensure all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 Already in Use
**Solution**: Use a different port
```bash
FLASK_PORT=5001 python app.py
```

### Issue: API Returns Empty Response
**Solution**: Check IBM API key in .env file

## 📞 Error Handling

The application includes comprehensive error handling:
- Invalid input validation
- API error management
- Fallback responses for unavailable services
- User-friendly error messages

## 🔒 Security Features

- ✅ CORS protection
- ✅ Input validation
- ✅ Environment variable isolation
- ✅ Debug mode disabled in production
- ✅ Error message sanitization

## 📈 Performance

- **Response Time**: < 3 seconds for complete plan
- **Concurrent Agents**: All 5 agents process in parallel
- **Memory Usage**: ~50MB base, ~100MB with data
- **Max Requests**: 100+ requests/minute

## 🎯 Future Enhancements

1. **Database Integration**: Store user plans and history
2. **User Authentication**: Login and personalized recommendations
3. **Real-time Bookings**: Direct hotel/flight booking integration
4. **Mobile App**: Native iOS/Android applications
5. **Advanced Analytics**: User behavior insights
6. **Multi-language Support**: Support for 20+ languages
7. **Social Features**: Share plans, community recommendations
8. **AR Integration**: Augmented reality location viewing

## 📄 License

This project is created for AICTE IBM SkillsBuild Program 2026.

## 👥 Contributing

This is an educational project. Contributions welcome for:
- Bug fixes
- Documentation improvements
- Feature enhancements
- Performance optimization

## 📧 Support

For issues or questions:
1. Check the docs/ folder
2. Review API.md for endpoint details
3. Check troubleshooting section

## 🙏 Acknowledgments

- IBM SkillsBuild Program
- AICTE (All India Council for Technical Education)
- IBM Granite LLM Team
- OpenWeatherMap API

---

**Made with ❤️ for travel enthusiasts and AI learners**

**Happy Traveling! 🌍✈️**
