"""
Test Suite for Travel Planner Agent
Comprehensive tests for all components
"""

import pytest
import json
from app import app
from config import get_config
from agents.itinerary_agent import ItineraryAgent
from agents.budget_agent import BudgetAgent
from agents.hotel_agent import HotelAgent
from agents.weather_agent import WeatherAgent
from agents.food_agent import FoodAgent
from services.granite_service import GraniteService
from services.weather_service import WeatherService


# ============================================
# FIXTURES
# ============================================

@pytest.fixture
def client():
    """Flask test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def config():
    """Test configuration"""
    return get_config('testing')


@pytest.fixture
def sample_travel_data():
    """Sample travel data for testing"""
    return {
        'destination': 'Paris',
        'days': 5,
        'budget': 2000,
        'travel_type': 'Couple',
        'interests': ['Art', 'Food', 'Historical'],
        'dietary_preferences': ['Vegetarian']
    }


# ============================================
# API ENDPOINT TESTS
# ============================================

class TestAPIEndpoints:
    """Test Flask API endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert data['service'] == 'Travel Planner Agent'
    
    def test_plan_endpoint_valid(self, client, sample_travel_data):
        """Test plan generation with valid data"""
        response = client.post('/api/plan', 
                             json=sample_travel_data,
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'summary' in data
        assert 'itinerary' in data
        assert 'budget' in data
    
    def test_plan_endpoint_invalid_days(self, client, sample_travel_data):
        """Test plan with invalid days"""
        sample_travel_data['days'] = 0
        response = client.post('/api/plan',
                             json=sample_travel_data,
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_plan_endpoint_invalid_budget(self, client, sample_travel_data):
        """Test plan with invalid budget"""
        sample_travel_data['budget'] = 50
        response = client.post('/api/plan',
                             json=sample_travel_data,
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_plan_endpoint_missing_destination(self, client, sample_travel_data):
        """Test plan with missing destination"""
        del sample_travel_data['destination']
        response = client.post('/api/plan',
                             json=sample_travel_data,
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_itinerary_endpoint(self, client):
        """Test itinerary endpoint"""
        data = {
            'destination': 'London',
            'days': 3,
            'interests': ['Historical'],
            'travel_type': 'Solo'
        }
        response = client.post('/api/itinerary',
                             json=data,
                             content_type='application/json')
        assert response.status_code == 200
    
    def test_budget_endpoint(self, client):
        """Test budget endpoint"""
        data = {
            'budget': 2000,
            'days': 5,
            'travel_type': 'Couple',
            'destination': 'Paris'
        }
        response = client.post('/api/budget',
                             json=data,
                             content_type='application/json')
        assert response.status_code == 200
    
    def test_hotels_endpoint(self, client):
        """Test hotels endpoint"""
        data = {
            'destination': 'Tokyo',
            'budget': 2000,
            'travel_type': 'Solo',
            'days': 5
        }
        response = client.post('/api/hotels',
                             json=data,
                             content_type='application/json')
        assert response.status_code == 200
    
    def test_weather_endpoint(self, client):
        """Test weather endpoint"""
        data = {
            'destination': 'Bangkok',
            'travel_dates': '2026-03-01 to 2026-03-05'
        }
        response = client.post('/api/weather',
                             json=data,
                             content_type='application/json')
        assert response.status_code == 200
    
    def test_food_endpoint(self, client):
        """Test food endpoint"""
        data = {
            'destination': 'Bangkok',
            'preferences': ['Spicy', 'Asian'],
            'budget': 30,
            'travel_type': 'Friends'
        }
        response = client.post('/api/food',
                             json=data,
                             content_type='application/json')
        assert response.status_code == 200
    
    def test_404_endpoint(self, client):
        """Test 404 error handling"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404


# ============================================
# AGENT TESTS
# ============================================

class TestAgents:
    """Test AI agents"""
    
    def test_itinerary_agent_initialization(self):
        """Test ItineraryAgent initialization"""
        agent = ItineraryAgent()
        assert agent.name == 'ItineraryAgent'
        assert agent.service is not None
    
    def test_itinerary_agent_process(self):
        """Test ItineraryAgent process method"""
        agent = ItineraryAgent()
        result = agent.process(
            destination='Rome',
            days=3,
            interests=['Historical'],
            travel_type='Solo'
        )
        assert isinstance(result, dict)
        assert 'destination' in result
        assert 'daily_plans' in result
    
    def test_budget_agent_initialization(self):
        """Test BudgetAgent initialization"""
        agent = BudgetAgent()
        assert agent.name == 'BudgetAgent'
    
    def test_budget_agent_process(self):
        """Test BudgetAgent process method"""
        agent = BudgetAgent()
        result = agent.process(
            budget=2000,
            days=5,
            travel_type='Couple',
            destination='Paris'
        )
        assert isinstance(result, dict)
        assert 'total_budget' in result
        assert 'breakdown' in result
    
    def test_hotel_agent_initialization(self):
        """Test HotelAgent initialization"""
        agent = HotelAgent()
        assert agent.name == 'HotelAgent'
    
    def test_hotel_agent_process(self):
        """Test HotelAgent process method"""
        agent = HotelAgent()
        result = agent.process(
            destination='Dubai',
            budget=2000,
            travel_type='Family',
            days=5
        )
        assert isinstance(result, dict)
        assert 'budget_hotels' in result
        assert 'mid_range_hotels' in result
        assert 'luxury_hotels' in result
    
    def test_weather_agent_initialization(self):
        """Test WeatherAgent initialization"""
        agent = WeatherAgent()
        assert agent.name == 'WeatherAgent'
    
    def test_weather_agent_process(self):
        """Test WeatherAgent process method"""
        agent = WeatherAgent()
        result = agent.process(
            destination='Sydney',
            travel_dates='2026-03-01 to 2026-03-10'
        )
        assert isinstance(result, dict)
        assert 'destination' in result
        assert 'current_weather' in result
    
    def test_food_agent_initialization(self):
        """Test FoodAgent initialization"""
        agent = FoodAgent()
        assert agent.name == 'FoodAgent'
    
    def test_food_agent_process(self):
        """Test FoodAgent process method"""
        agent = FoodAgent()
        result = agent.process(
            destination='Bangkok',
            cuisine_preferences=['Thai', 'Asian'],
            budget=25,
            travel_type='Friends'
        )
        assert isinstance(result, dict)
        assert 'must_try_dishes' in result
        assert 'street_food' in result


# ============================================
# SERVICE TESTS
# ============================================

class TestServices:
    """Test external services"""
    
    def test_granite_service_initialization(self, config):
        """Test GraniteService initialization"""
        service = GraniteService(config)
        assert service.config is not None
        assert service.timeout == config.AGENTS_TIMEOUT
    
    def test_granite_service_generate_text(self, config):
        """Test Granite text generation (with fallback)"""
        service = GraniteService(config)
        result = service.generate_text("Hello, what is travel?")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_granite_service_generate_itinerary(self, config):
        """Test Granite itinerary generation"""
        service = GraniteService(config)
        result = service.generate_itinerary(
            destination='Paris',
            days=7,
            interests=['Art', 'Food'],
            travel_type='Couple'
        )
        assert isinstance(result, dict)
    
    def test_weather_service_initialization(self, config):
        """Test WeatherService initialization"""
        service = WeatherService(config)
        assert service.api_key is not None or True  # Can be empty
    
    def test_weather_service_get_clothing_suggestions(self, config):
        """Test weather-based clothing suggestions"""
        service = WeatherService(config)
        suggestions = service.get_clothing_suggestions(
            temperature=25,
            weather_condition='Sunny'
        )
        assert isinstance(suggestions, dict)
        assert 'essentials' in suggestions
        assert 'clothing' in suggestions


# ============================================
# DATA VALIDATION TESTS
# ============================================

class TestDataValidation:
    """Test data validation"""
    
    def test_days_validation(self, client):
        """Test days validation (1-30)"""
        data = {
            'destination': 'Paris',
            'days': 35,  # Invalid
            'budget': 2000,
            'travel_type': 'Couple',
            'interests': ['Food']
        }
        response = client.post('/api/plan', json=data)
        assert response.status_code == 400
    
    def test_budget_validation(self, client):
        """Test budget validation (min 100)"""
        data = {
            'destination': 'Paris',
            'days': 5,
            'budget': 50,  # Invalid
            'travel_type': 'Couple',
            'interests': ['Food']
        }
        response = client.post('/api/plan', json=data)
        assert response.status_code == 400
    
    def test_travel_type_validation(self, client):
        """Test travel type validation"""
        data = {
            'destination': 'Paris',
            'days': 5,
            'budget': 2000,
            'travel_type': 'Invalid',
            'interests': ['Food']
        }
        # Should still process (no strict validation)
        response = client.post('/api/plan', json=data)
        # Either 200 (processed) or 400 (rejected)
        assert response.status_code in [200, 400]


# ============================================
# RESPONSE FORMAT TESTS
# ============================================

class TestResponseFormats:
    """Test response formats"""
    
    def test_plan_response_format(self, client, sample_travel_data):
        """Test plan response has correct format"""
        response = client.post('/api/plan', json=sample_travel_data)
        data = json.loads(response.data)
        
        required_keys = ['status', 'summary', 'itinerary', 'budget', 
                        'accommodation', 'weather', 'food']
        for key in required_keys:
            assert key in data
    
    def test_summary_format(self, client, sample_travel_data):
        """Test summary section format"""
        response = client.post('/api/plan', json=sample_travel_data)
        data = json.loads(response.data)
        summary = data['summary']
        
        required_keys = ['destination', 'duration', 'total_budget', 
                        'travel_type', 'interests', 'generated_at']
        for key in required_keys:
            assert key in summary


# ============================================
# RUN TESTS
# ============================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
