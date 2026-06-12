# 🏗️ System Architecture - Travel Planner Agent

## Overview
The Travel Planner Agent follows a modular, agent-based architecture designed for scalability and maintainability.

## Architecture Layers

### 1. Presentation Layer (Frontend)
```
┌─────────────────────────────────────┐
│      Web Browser (HTML/CSS/JS)      │
├─────────────────────────────────────┤
│   - Responsive UI                   │
│   - Form Input Validation            │
│   - Real-time Display                │
│   - Export Functionality             │
└─────────────────────────────────────┘
            ↓ HTTP/AJAX
```

### 2. Application Layer (Backend)
```
┌──────────────────────────────────────┐
│     Flask Web Server (app.py)        │
├──────────────────────────────────────┤
│  Route Handlers:                     │
│  ├── POST /api/plan                  │
│  ├── POST /api/itinerary             │
│  ├── POST /api/budget                │
│  ├── POST /api/hotels                │
│  ├── POST /api/weather               │
│  └── POST /api/food                  │
└──────────────────────────────────────┘
        ↓ Orchestration
```

### 3. Agent Layer
```
┌─────────────────────────────────────┐
│     Agent Orchestration System      │
├─────────────────────────────────────┤
│  ┌─────────────┬─────────────┐      │
│  │  Itinerary  │   Budget    │      │
│  │    Agent    │    Agent    │      │
│  └─────────────┴─────────────┘      │
│  ┌─────────────┬─────────────┐      │
│  │    Hotel    │   Weather   │      │
│  │    Agent    │    Agent    │      │
│  └─────────────┴─────────────┘      │
│  ┌─────────────┐                    │
│  │    Food     │                    │
│  │    Agent    │                    │
│  └─────────────┘                    │
└─────────────────────────────────────┘
        ↓ Data Processing
```

### 4. Service Layer
```
┌──────────────────────────────────────┐
│       External Services              │
├──────────────────────────────────────┤
│  ├── Granite LLM Service             │
│  │   └─ IBM Cloud Watson             │
│  │                                   │
│  ├── Weather Service                 │
│  │   └─ OpenWeatherMap API           │
│  │                                   │
│  └── Data Processing                 │
│      └─ Formatting & Parsing         │
└──────────────────────────────────────┘
        ↓ External APIs
```

### 5. Data Layer
```
┌──────────────────────────────────────┐
│      Data Storage & Caching          │
├──────────────────────────────────────┤
│  ├── In-Memory Cache                 │
│  ├── Session Storage                 │
│  └── Configuration Data              │
└──────────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────────────┐
│   User Input    │ (via HTML Form)
└────────┬────────┘
         │
         ↓
┌──────────────────────────┐
│   Form Validation        │
│   & Data Processing      │
└────────┬─────────────────┘
         │
         ↓
    ┌────────────────────────────────────────────┐
    │  Initialize All 5 Agents in Parallel       │
    └────┬─────────┬──────────┬────────┬────────┘
         │         │          │        │
    ┌────▼─┐  ┌────▼──┐  ┌───▼──┐ ┌──▼──┐  ┌────▼──┐
    │Itine  │  │Budget │  │Hotel │ │Weath│  │ Food  │
    │raryA  │  │ Agent │  │Agent │ │er A │  │ Agent │
    │gent   │  │       │  │      │ │gent │  │       │
    └────┬──┘  └───┬──┘  └──┬───┘ └──┬──┘  └───┬────┘
         │         │        │       │         │
         └─────────┼────────┼───────┼─────────┘
                   │
                   ↓
        ┌───────────────────────┐
        │  Process Results      │
        │  Aggregate Data       │
        └───────────┬───────────┘
                    │
                    ↓
           ┌────────────────────┐
           │  JSON Response     │
           └────────────┬───────┘
                        │
                        ↓
           ┌────────────────────────┐
           │  Frontend Rendering    │
           │  Display to User       │
           └────────────────────────┘
```

## Component Interaction

```
    ┌─────────────────────────────────────────┐
    │        Frontend (HTML/CSS/JS)           │
    │  ┌────────────────────────────────────┐ │
    │  │  • User Form                       │ │
    │  │  • Display Results                 │ │
    │  │  • Tab Navigation                  │ │
    │  │  • Export Options                  │ │
    │  └────────────────────────────────────┘ │
    └────────────┬────────────────────────────┘
                 │ HTTP POST/GET
                 ↓
    ┌─────────────────────────────────────────┐
    │        Flask Backend (app.py)           │
    │  ┌────────────────────────────────────┐ │
    │  │  @app.route('/api/plan')           │ │
    │  │  ├─ Validate Input                 │ │
    │  │  ├─ Instantiate Agents             │ │
    │  │  ├─ Process Requests               │ │
    │  │  └─ Return JSON                    │ │
    │  └────────────────────────────────────┘ │
    └────────────┬────────────────────────────┘
                 │
    ┌────────────┴────────────────────────────┐
    │                                         │
    ↓                                         ↓
┌──────────────────┐                ┌──────────────────────┐
│  Agent Layer     │                │  Service Layer       │
│  ┌─────────────────────────────┐  │  ┌──────────────────┐│
│  │ • ItineraryAgent            │  │  │ GraniteService   ││
│  │ • BudgetAgent               │  │  │ WeatherService   ││
│  │ • HotelAgent                │  │  │ TravelWeatherA   ││
│  │ • WeatherAgent              │  │  └──────────────────┘│
│  │ • FoodAgent                 │  └──────────────────────┘
│  └─────────────────────────────┘           ↓
│           ⧘                       External APIs
└──────────────────┘
```

## Module Responsibilities

### config.py
- Manages environment variables
- Provides configuration classes for different environments
- Handles API keys and URLs

### agents/
Each agent module handles specific travel planning aspects:
- **itinerary_agent.py**: Day-wise schedule creation
- **budget_agent.py**: Expense breakdown and optimization
- **hotel_agent.py**: Accommodation recommendations
- **weather_agent.py**: Weather data and clothing suggestions
- **food_agent.py**: Local cuisine and dining recommendations

### services/
- **granite_service.py**: IBM Granite LLM integration
- **weather_service.py**: OpenWeatherMap API integration

### app.py
- Main Flask application
- Route definitions
- Request/response handling
- Error management

### templates/
- **index.html**: Single-page application template
- Form interface
- Results display tabs
- Export options

### static/
- **style.css**: Responsive design
- **script.js**: Client-side logic and API integration
- **images/**: Visual assets

## Data Structures

### Input Data Structure
```python
{
    "destination": str,
    "days": int,
    "budget": float,
    "travel_type": str,  # Solo, Family, Friends, Couple
    "interests": list,   # Multiple interests
    "dietary_preferences": list,
    "source_location": str (optional)
}
```

### Output Data Structure
```python
{
    "status": "success",
    "summary": {
        "destination": str,
        "duration": int,
        "total_budget": float,
        "travel_type": str,
        "interests": list,
        "generated_at": str (ISO 8601)
    },
    "itinerary": {...},    # Day-wise plans
    "budget": {...},       # Expense breakdown
    "accommodation": {...},# Hotel recommendations
    "weather": {...},      # Weather information
    "food": {...},         # Food recommendations
    "emergency_info": {...}# Safety & emergency contacts
}
```

## Sequence Diagram

```
User    Frontend    Backend    Agents    Services
 │         │          │         │          │
 ├────── Form Fill ──→│         │          │
 │         │          │         │          │
 ├─ Submit ──→│         │         │          │
 │         │          │         │          │
 │         │ Validate ─→│         │          │
 │         │          │ Process ──→│          │
 │         │          │───Itinerary──→│      │
 │         │          │───Budget─────→│      │
 │         │          │───Hotel──────→│      │
 │         │          │───Weather────→│      │
 │         │          │───Food───────→│      │
 │         │          │              │ Call API
 │         │          │              │──→│
 │         │          │  Aggregate Results
 │         │← JSON Response ─────│          │
 │← Display Results ──│          │          │
 │ View Tabs   Plan   │          │          │
 │ Export Option      │          │          │
```

## Error Handling Flow

```
        ┌─────────────────┐
        │  User Input     │
        └────────┬────────┘
                 │
                 ↓
        ┌─────────────────────┐
        │  Validation Check   │
        └────────┬────────┬───┘
                 │        │
            Valid│        │Invalid
                 │        └──→ Return 400 Error
                 ↓
        ┌─────────────────┐
        │  Process Data   │
        └────────┬────────┘
                 │
                 ↓
        ┌──────────────────────┐
        │  Call External APIs  │
        └────────┬────────┬────┘
                 │        │
             Success      │Failure
                 │        └──→ Fallback Response
                 ↓
        ┌─────────────────┐
        │  Return 200 OK  │
        └─────────────────┘
```

## Scalability Considerations

### Horizontal Scaling
```
Original:
    ┌──────────┐
    │ Server 1 │
    └──────────┘

Scaled:
    ┌──────────┐
    │ Server 1 │
    └──┬───────┘
       │
    ┌──┴──────┐
    │ LoadB   │
    │ alancer │
    └──┬─────┬┘
       │     │
    ┌──▼──┐┌─▼───┐
    │Serv │ Serv │
    │er 2 │ er 3 │
    └─────┴──────┘
```

### Vertical Scaling
- Increase Python worker threads
- Use thread pool executors
- Implement caching mechanisms

### Database Optimization
- Index frequently queried fields
- Implement query caching
- Use connection pooling

## Security Architecture

```
┌─────────────────────────────────┐
│   Network Layer                 │
│   • HTTPS/TLS                   │
│   • CORS Protection             │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│   Application Layer             │
│   • Input Validation            │
│   • Sanitization                │
│   • Error Handling              │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│   Service Layer                 │
│   • API Key Management          │
│   • Secure Credentials          │
│   • Environment Variables       │
└─────────────────────────────────┘
```

## Performance Metrics

- **Request Response Time**: ~2-3 seconds
- **Agent Processing**: Parallel execution (all 5 agents)
- **Memory Usage**: ~100MB with full data
- **Concurrent Connections**: 100+

---

**Architecture Documentation v1.0** | Travel Planner Agent
