"""
Travel Planner Orchestrator

Provides a ConversationManager that extracts structured trip parameters
from user queries (via Granite), calls specialized services/agents,
and maintains simple in-memory conversation memory for follow-ups.

This file is intentionally lightweight and uses existing services in
`services/` and `agents/`.
"""
from typing import Dict, Any, Optional
import uuid
import traceback

from services.granite_service import GraniteService
from services.weather_service import TravelWeatherAnalyzer
from agents.itinerary_agent import ItineraryAgent
from agents.budget_agent import BudgetAgent
from agents.hotel_agent import HotelAgent
from agents.food_agent import FoodAgent
from config import get_config


class ConversationManager:
    """Manage short-lived conversation memory and orchestrate agents."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.granite = GraniteService(self.config)
        self.weather_analyzer = TravelWeatherAnalyzer(self.config)
        # Lightweight agents - reuse existing implementations
        self.itinerary_agent = ItineraryAgent(self.config)
        self.budget_agent = BudgetAgent(self.config)
        self.hotel_agent = HotelAgent(self.config)
        self.food_agent = FoodAgent(self.config)

        # In-memory conversation store: session_id -> list of messages/plans
        self.memory: Dict[str, Dict[str, Any]] = {}

    def _new_session(self) -> str:
        return str(uuid.uuid4())

    def extract_parameters(self, query: str) -> Dict[str, Any]:
        """Ask Granite to parse a free-text query into structured fields.

        The output is expected to be a JSON-like object with keys:
        destination, days, budget, month_or_dates, preferences (list).
        """
        try:
            prompt = f"""
            Extract travel parameters from the user query.
            Return a JSON object with keys: destination, days, budget, month_or_dates, preferences.
            Query: "{query}"

            Example JSON:
            {
              "destination": "Goa",
              "days": 5,
              "budget": 20000,
              "month_or_dates": "December",
              "preferences": ["beach", "food"]
            }
            """

            raw = self.granite.generate_text(prompt, max_tokens=400)
            parsed = self.granite._parse_json_response(raw)
            # Basic normalization
            if isinstance(parsed, dict):
                return parsed
            return {'destination': None, 'days': None, 'budget': None, 'month_or_dates': None, 'preferences': []}

        except Exception:
            traceback.print_exc()
            return {'destination': None, 'days': None, 'budget': None, 'month_or_dates': None, 'preferences': []}

    def create_plan_from_query(self, query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a full travel plan from a user query.

        Returns a dictionary containing itinerary, budget, hotels, weather and food.
        """
        if session_id is None:
            session_id = self._new_session()

        # Save initial user message
        self.memory[session_id] = {'user_queries': [query], 'plans': []}

        params = self.extract_parameters(query)
        destination = params.get('destination') or query
        days = int(params.get('days') or 3)
        budget = float(params.get('budget') or 1000)
        preferences = params.get('preferences') or []
        travel_type = params.get('travel_type') or 'Solo'
        month_or_dates = params.get('month_or_dates') or ''

        # Generate outputs using agents/services
        itinerary = self.itinerary_agent.process(destination, days, preferences, travel_type)
        budget_plan = self.budget_agent.process(budget, days, travel_type, destination)
        hotels = self.hotel_agent.process(destination, budget, travel_type, days)
        weather_info = self.weather_analyzer.analyze_travel_weather(destination, month_or_dates or f'Next {days} days')
        food_recs = self.food_agent.process(destination, preferences, budget/days, travel_type)

        from datetime import datetime

        plan = {
            'session_id': session_id,
            'query': query,
            'summary': {
                'destination': destination,
                'duration': days,
                'total_budget': budget,
                'travel_type': travel_type,
                'interests': preferences,
                'month_or_dates': month_or_dates,
                'generated_at': datetime.now().isoformat()
            },
            'itinerary': itinerary,
            'budget': budget_plan,
            'accommodation': hotels,
            'weather': weather_info,
            'food': food_recs
        }

        # Store plan in memory
        self.memory[session_id]['plans'].append(plan)

        return plan

    def follow_up(self, session_id: str, instruction: str) -> Dict[str, Any]:
        """Handle a follow-up instruction referencing previous plan.

        Example: "Make it cheaper" or "Add more adventure activities"
        """
        if session_id not in self.memory or not self.memory[session_id]['plans']:
            return {'error': 'No prior plan found for this session.'}

        last_plan = self.memory[session_id]['plans'][-1]

        # Create a prompt for Granite to modify the plan
        try:
            prompt = f"""
            You are a travel planner assistant. The user previously received this plan:
            {last_plan}

            The user asks: "{instruction}".
            Modify the plan accordingly and return a new full plan JSON with the same keys: summary, itinerary, budget, accommodation, weather, food.
            Keep the response as JSON only.
            """

            raw = self.granite.generate_text(prompt, max_tokens=1800)
            parsed = self.granite._parse_json_response(raw)
            if isinstance(parsed, dict):
                # store updated plan
                self.memory[session_id]['plans'].append(parsed)
                return parsed
            else:
                return {'error': 'Unable to parse modification response', 'raw': raw}

        except Exception as e:
            traceback.print_exc()
            return {'error': str(e)}


conversation_manager = ConversationManager()

if __name__ == '__main__':
    # quick manual test
    cm = ConversationManager()
    q = "Plan a 5-day trip to Goa in December under ₹20000"
    print(cm.create_plan_from_query(q))
