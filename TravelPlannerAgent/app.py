"""
Travel Planner Agent
Main Flask application
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from config import get_config
from agents.itinerary_agent import ItineraryAgent
from agents.budget_agent import BudgetAgent
from agents.hotel_agent import HotelAgent
from agents.weather_agent import WeatherAgent
from agents.food_agent import FoodAgent
from agent import conversation_manager
from services.claude_service import claude_service
from services.gemini_service import gemini_service
from services.granite_service import GraniteService

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
config = get_config(os.getenv('FLASK_ENV', 'development'))
app.config.from_object(config)

# Initialize agents
itinerary_agent = ItineraryAgent(config)
budget_agent = BudgetAgent(config)
hotel_agent = HotelAgent(config)
weather_agent = WeatherAgent(config)
food_agent = FoodAgent(config)


@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Travel Planner Agent'
    })


@app.route('/api/plan', methods=['POST'])
def create_travel_plan():
    """
    Create comprehensive travel plan
    
    Request body:
    {
        'source_location': string,
        'destination': string,
        'days': integer,
        'budget': float,
        'travel_type': string,
        'interests': list,
        'dietary_preferences': list
    }
    """
    try:
        data = request.get_json()

        # If user provided a free-text query (e.g., "Plan a 5-day trip to Goa..."), use ConversationManager
        if data and 'query' in data and data.get('query'):
            plan = conversation_manager.create_plan_from_query(data.get('query'))
            return jsonify(plan)

        # Structured input path (existing behavior)
        # Validate input
        required_fields = ['destination', 'days', 'budget', 'travel_type', 'interests']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        destination = data.get('destination', '').strip()
        days = int(data.get('days', 1))
        budget = float(data.get('budget', 0))
        travel_type = data.get('travel_type', 'Solo')
        interests = data.get('interests', [])
        dietary_preferences = data.get('dietary_preferences', [])

        # Validate constraints
        if days < 1 or days > 30:
            return jsonify({'error': 'Days should be between 1 and 30'}), 400
        if budget < 100:
            return jsonify({'error': 'Budget should be at least 100'}), 400
        if not destination:
            return jsonify({'error': 'Destination is required'}), 400

        # Call all agents
        itinerary = itinerary_agent.process(destination, days, interests, travel_type)
        budget_plan = budget_agent.process(budget, days, travel_type, destination)
        hotels = hotel_agent.process(destination, budget, travel_type, days)
        weather_info = weather_agent.process(destination, f'Next {days} days')
        food_recs = food_agent.process(destination, dietary_preferences or interests, budget/days, travel_type)

        # Compile comprehensive plan
        travel_plan = {
            'status': 'success',
            'summary': {
                'destination': destination,
                'duration': days,
                'total_budget': budget,
                'travel_type': travel_type,
                'interests': interests,
                'generated_at': datetime.now().isoformat()
            },
            'itinerary': itinerary,
            'budget': budget_plan,
            'accommodation': hotels,
            'weather': weather_info,
            'food': food_recs,
            'emergency_info': {
                'emergency_contacts': weather_agent.service.generate_emergency_contacts(
                    destination, 'Country'
                ),
                'safety_tips': weather_agent.service.generate_safety_tips(destination, travel_type)
            }
        }

        return jsonify(travel_plan)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        print(f"Error creating travel plan: {str(e)}")
        return jsonify({'error': 'Internal server error', 'detail': str(e)}), 500


@app.route('/api/itinerary', methods=['POST'])
def get_itinerary():
    """Get itinerary details"""
    try:
        data = request.get_json()
        destination = data.get('destination')
        days = int(data.get('days', 1))
        interests = data.get('interests', [])
        travel_type = data.get('travel_type', 'Solo')
        
        itinerary = itinerary_agent.process(destination, days, interests, travel_type)
        return jsonify(itinerary)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/budget', methods=['POST'])
def get_budget():
    """Get budget breakdown"""
    try:
        data = request.get_json()
        budget = float(data.get('budget'))
        days = int(data.get('days', 1))
        travel_type = data.get('travel_type', 'Solo')
        destination = data.get('destination', '')
        
        budget_plan = budget_agent.process(budget, days, travel_type, destination)
        return jsonify(budget_plan)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/hotels', methods=['POST'])
def get_hotels():
    """Get hotel recommendations"""
    try:
        data = request.get_json()
        destination = data.get('destination')
        budget = float(data.get('budget'))
        travel_type = data.get('travel_type', 'Solo')
        days = int(data.get('days', 1))
        
        hotels = hotel_agent.process(destination, budget, travel_type, days)
        return jsonify(hotels)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/weather', methods=['POST'])
def get_weather():
    """Get weather information"""
    try:
        data = request.get_json()
        destination = data.get('destination')
        travel_dates = data.get('travel_dates', 'Next 5 days')
        
        weather_info = weather_agent.process(destination, travel_dates)
        return jsonify(weather_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/food', methods=['POST'])
def get_food_recommendations():
    """Get food recommendations"""
    try:
        data = request.get_json()
        destination = data.get('destination')
        preferences = data.get('preferences', [])
        budget = float(data.get('budget', 20))
        travel_type = data.get('travel_type', 'Solo')
        
        food_recs = food_agent.process(destination, preferences, budget, travel_type)
        return jsonify(food_recs)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat_with_model():
    """Chat endpoint that forwards messages to selected model provider.

    Body: { 'provider': 'granite'|'claude'|'gemini', 'message': '...' }
    """
    try:
        data = request.get_json() or {}
        provider = data.get('provider', 'granite')
        message = data.get('message', '')
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        if provider == 'claude':
            resp = claude_service.generate_text(message)
        elif provider == 'gemini':
            resp = gemini_service.generate_text(message)
        else:
            # default to Granite
            granite = GraniteService(app.config)
            resp = granite.generate_text(message)

        return jsonify({'provider': provider, 'response': resp})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/packing-checklist', methods=['POST'])
def get_packing_checklist():
    """Get packing checklist"""
    try:
        data = request.get_json()
        destination = data.get('destination')
        days = int(data.get('days', 1))
        weather = data.get('weather', 'Moderate')
        
        checklist = itinerary_agent.service.generate_packing_checklist(
            destination, days, weather
        )
        
        return jsonify({
            'destination': destination,
            'duration': days,
            'weather': weather,
            'checklist': checklist
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Get debug mode from config
    debug_mode = app.config.get('DEBUG', False)
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print("=" * 60)
    print("🧳 Travel Planner Agent - Starting Server")
    print("=" * 60)
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Debug Mode: {debug_mode}")
    print(f"Port: {port}")
    print(f"URL: http://localhost:{port}")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
