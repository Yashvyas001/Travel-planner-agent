"""
Itinerary Agent
Generates day-wise travel itinerary
"""

from typing import Dict, Any, List
from services.granite_service import GraniteAgent

class ItineraryAgent(GraniteAgent):
    """Agent for generating travel itineraries"""
    
    def __init__(self, config=None):
        """Initialize Itinerary Agent"""
        super().__init__("ItineraryAgent", config)
    
    def process(self, destination: str, days: int, interests: List[str], 
               travel_type: str) -> Dict[str, Any]:
        """
        Generate day-wise itinerary
        
        Args:
            destination: Travel destination
            days: Number of days
            interests: List of interests
            travel_type: Type of travel (Solo, Family, Friends, Couple)
            
        Returns:
            Itinerary dictionary
        """
        self.log(f"Generating {days}-day itinerary for {destination}")
        self.log(f"Travel Type: {travel_type}, Interests: {interests}")
        
        # Get itinerary from Granite
        itinerary_data = self.service.generate_itinerary(
            destination, days, interests, travel_type
        )
        
        # Structure the itinerary
        itinerary = {
            'destination': destination,
            'duration': days,
            'travel_type': travel_type,
            'interests': interests,
            'daily_plans': self._structure_daily_plans(days, itinerary_data),
            'highlights': self._extract_highlights(itinerary_data),
            'transportation': self._suggest_transportation(travel_type),
            'best_times': self._get_best_visiting_times(destination)
        }
        
        self.log("Itinerary generated successfully")
        return itinerary
    
    def _structure_daily_plans(self, days: int, itinerary_data: Dict) -> List[Dict[str, Any]]:
        """
        Structure daily plans
        
        Args:
            days: Number of days
            itinerary_data: Raw itinerary data from Granite
            
        Returns:
            List of daily plans
        """
        daily_plans = []
        
        for day in range(1, days + 1):
            plan = {
                'day': day,
                'morning': {
                    'activity': f'Morning activities for day {day}',
                    'time': '07:00 - 12:00',
                    'location': '',
                    'notes': 'Start the day early to maximize exploration'
                },
                'afternoon': {
                    'activity': f'Afternoon exploration for day {day}',
                    'time': '12:00 - 17:00',
                    'location': '',
                    'notes': 'Lunch and relaxation time included'
                },
                'evening': {
                    'activity': f'Evening activities for day {day}',
                    'time': '17:00 - 22:00',
                    'location': '',
                    'notes': 'Dinner and leisure activities'
                },
                'meals': {
                    'breakfast': 'Hotel breakfast',
                    'lunch': 'Local restaurant',
                    'dinner': 'Regional specialty restaurant'
                },
                'travel_time': '30 minutes',
                'estimated_cost': '$50-100'
            }
            daily_plans.append(plan)
        
        return daily_plans
    
    def _extract_highlights(self, itinerary_data: Dict) -> List[str]:
        """Extract key highlights from itinerary"""
        highlights = [
            'Visit major tourist attractions',
            'Experience local culture',
            'Taste authentic local cuisine',
            'Interact with local communities',
            'Capture memorable photographs'
        ]
        return highlights
    
    def _suggest_transportation(self, travel_type: str) -> Dict[str, list]:
        """
        Suggest transportation options based on travel type
        
        Args:
            travel_type: Type of travel
            
        Returns:
            Transportation suggestions
        """
        suggestions = {
            'within_city': [
                'Public transportation (Buses, Metro)',
                'Taxis/Uber',
                'Bicycles',
                'Walking tours'
            ],
            'between_cities': [
                'Trains',
                'Buses',
                'Flights (if far)',
                'Rental cars'
            ],
            'local_transport': [
                'Auto-rickshaws',
                'Local buses',
                'Hired cars',
                'Tour buses'
            ]
        }
        return suggestions
    
    def _get_best_visiting_times(self, destination: str) -> Dict[str, str]:
        """
        Get best times to visit destination
        
        Args:
            destination: Destination name
            
        Returns:
            Best visiting times information
        """
        return {
            'best_season': 'October to March (for most destinations)',
            'peak_season': 'December to February',
            'off_season': 'May to September',
            'weather_consideration': 'Check monsoon/weather patterns',
            'cultural_events': 'Research local festivals during travel dates'
        }
