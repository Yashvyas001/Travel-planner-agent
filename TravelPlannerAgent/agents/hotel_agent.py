"""
Hotel Agent
Recommends hotels based on budget and preferences
"""

from typing import Dict, Any, List
from services.granite_service import GraniteAgent
from services.places_service import get_famous_places, get_viral_dhabas

# Curated hotel DB to enrich recommendations
HOTEL_DB = {
    'delhi': {
        'budget': [
            {'name': 'Zostel Delhi', 'price_per_night': '₹500-900'},
            {'name': 'FabHotel Prime', 'price_per_night': '₹1200-1800'}
        ],
        'mid_range': [
            {'name': 'Lemon Tree Hotel', 'price_per_night': '₹4000-6000'},
            {'name': 'Radisson Blu', 'price_per_night': '₹6000-9000'}
        ],
        'luxury': [
            {'name': 'The Lodhi', 'price_per_night': '₹25000-40000'},
            {'name': 'ITC Maurya', 'price_per_night': '₹20000-35000'}
        ]
    },
    'goa': {
        'budget': [
            {'name': 'Zostel Goa', 'price_per_night': '₹600-1200'}
        ],
        'mid_range': [
            {'name': 'Treebo Trend', 'price_per_night': '₹2500-4000'}
        ],
        'luxury': [
            {'name': 'Taj Exotica Resort', 'price_per_night': '₹18000-30000'}
        ]
    },
    'jaipur': {
        'budget': [
            {'name': 'Zostel Jaipur', 'price_per_night': '₹500-1000'}
        ],
        'mid_range': [
            {'name': 'Trident Jaipur', 'price_per_night': '₹6000-9000'}
        ],
        'luxury': [
            {'name': 'Rambagh Palace', 'price_per_night': '₹35000-60000'}
        ]
    }
}

class HotelAgent(GraniteAgent):
    """Agent for hotel recommendations"""
    
    def __init__(self, config=None):
        """Initialize Hotel Agent"""
        super().__init__("HotelAgent", config)
    
    def process(self, destination: str, budget: float, travel_type: str,
               days: int) -> Dict[str, Any]:
        """
        Recommend hotels based on parameters
        
        Args:
            destination: Travel destination
            budget: Total budget
            travel_type: Type of travel
            days: Number of days
            
        Returns:
            Hotel recommendations dictionary
        """
        self.log(f"Finding hotels in {destination} with budget ${budget}")
        self.log(f"Travel Type: {travel_type}, Duration: {days} days")
        
        daily_hotel_budget = (budget * 0.35) / days  # 35% of budget for hotels
        
        # Fetch popular places and viral dhabas for the destination
        famous_places = get_famous_places(destination)
        viral_dhabas = get_viral_dhabas(destination)

        # Base lists from generators
        base_budget = self._get_budget_hotels(destination, daily_hotel_budget)
        base_mid = self._get_mid_range_hotels(destination, daily_hotel_budget)
        base_lux = self._get_luxury_hotels(destination, daily_hotel_budget)
        base_lux = self._enhance_luxury_list(destination, base_lux, daily_hotel_budget)

        # Enrich with curated DB entries if present for the city
        key = destination.lower().strip()
        city_hotels = HOTEL_DB.get(key)
        if city_hotels:
            def map_entry(e, typ):
                return {
                    'name': e.get('name'),
                    'price_per_night': e.get('price_per_night'),
                    'rating': 4.5,
                    'type': typ,
                    'location': 'Recommended Area',
                    'amenities': ['WiFi', 'Breakfast'],
                    'check_in': '14:00',
                    'check_out': '11:00',
                    'cancellation': 'Check policy',
                    'pros': ['Recommended'],
                    'cons': []
                }

            enriched_budget = [map_entry(e, 'Budget Hotel') for e in city_hotels.get('budget', [])]
            enriched_mid = [map_entry(e, 'Mid-Range Hotel') for e in city_hotels.get('mid_range', [])]
            enriched_lux = [map_entry(e, 'Luxury Hotel') for e in city_hotels.get('luxury', [])]

            budget_list = enriched_budget + base_budget
            mid_list = enriched_mid + base_mid
            lux_list = enriched_lux + base_lux
        else:
            budget_list = base_budget
            mid_list = base_mid
            lux_list = base_lux

        recommendations = {
            'destination': destination,
            'budget_allocation': budget * 0.35,
            'daily_hotel_budget': round(daily_hotel_budget, 2),
            'travel_type': travel_type,
            'budget_hotels': budget_list,
            'mid_range_hotels': mid_list,
            'luxury_hotels': lux_list,
            'booking_tips': self._get_booking_tips(),
            'amenities_guide': self._get_amenities_by_type(travel_type),
            'location_recommendations': self._get_location_recommendations(destination),
            'famous_places': famous_places,
            'viral_dhabas': viral_dhabas
        }
        
        self.log("Hotel recommendations generated")
        return recommendations
    
    def _get_budget_hotels(self, destination: str, daily_budget: float) -> List[Dict[str, Any]]:
        """
        Get budget hotel recommendations
        
        Args:
            destination: Destination
            daily_budget: Daily budget
            
        Returns:
            List of budget hotels
        """
        return [
            {
                'name': f'{destination} Budget Inn',
                'price_per_night': round(daily_budget * 0.7, 2),
                'rating': 3.8,
                'type': 'Budget Hotel',
                'location': 'City Center',
                'amenities': ['WiFi', 'Air Conditioning', 'Basic Breakfast', 'Parking'],
                'check_in': '14:00',
                'check_out': '11:00',
                'cancellation': 'Free cancellation up to 24 hours',
                'pros': ['Affordable', 'Clean rooms', 'Good location', 'Helpful staff'],
                'cons': ['Small rooms', 'Limited amenities', 'No AC in some rooms']
            },
            {
                'name': f'{destination} Hostel',
                'price_per_night': round(daily_budget * 0.5, 2),
                'rating': 4.2,
                'type': 'Hostel',
                'location': 'Near Bus Station',
                'amenities': ['WiFi', 'Common Kitchen', 'Lockers', 'Social Areas'],
                'check_in': '15:00',
                'check_out': '10:00',
                'cancellation': 'Free cancellation',
                'pros': ['Very cheap', 'Social atmosphere', 'Kitchen access', 'Great for solo travelers'],
                'cons': ['Shared bathrooms', 'Crowded at peak times', 'Limited privacy']
            },
            {
                'name': f'{destination} Guesthouse',
                'price_per_night': round(daily_budget * 0.6, 2),
                'rating': 4.0,
                'type': 'Guesthouse',
                'location': 'Residential Area',
                'amenities': ['WiFi', 'Breakfast', 'Laundry', 'Local Advice'],
                'check_in': '13:00',
                'check_out': '11:00',
                'cancellation': 'Free cancellation up to 24 hours',
                'pros': ['Homely feel', 'Local experience', 'Budget-friendly', 'Personal service'],
                'cons': ['Limited amenities', 'May be far from center', 'Less privacy']
            }
        ]
    
    def _get_mid_range_hotels(self, destination: str, daily_budget: float) -> List[Dict[str, Any]]:
        """
        Get mid-range hotel recommendations
        
        Args:
            destination: Destination
            daily_budget: Daily budget
            
        Returns:
            List of mid-range hotels
        """
        return [
            {
                'name': f'{destination} Plaza Hotel',
                'price_per_night': round(daily_budget * 1.2, 2),
                'rating': 4.3,
                'type': 'Mid-Range Hotel',
                'location': 'City Center',
                'amenities': ['WiFi', 'Air Conditioning', 'Restaurant', 'Gym', 'Business Center'],
                'check_in': '14:00',
                'check_out': '12:00',
                'cancellation': 'Free cancellation up to 48 hours',
                'pros': ['Good location', 'Good value', 'Multiple amenities', 'Good customer service'],
                'cons': ['Can be crowded', 'Limited parking']
            },
            {
                'name': f'{destination} Heritage Hotel',
                'price_per_night': round(daily_budget * 1.1, 2),
                'rating': 4.4,
                'type': 'Heritage Hotel',
                'location': 'Historic District',
                'amenities': ['WiFi', 'Restaurant', 'Spa', 'Bar', 'Heritage Tours'],
                'check_in': '14:00',
                'check_out': '11:00',
                'cancellation': 'Free cancellation up to 48 hours',
                'pros': ['Cultural experience', 'Beautiful building', 'Good restaurant', 'Unique stay'],
                'cons': ['Can be pricey', 'Old building amenities']
            },
            {
                'name': f'{destination} Comfort Inn',
                'price_per_night': round(daily_budget * 1.0, 2),
                'rating': 4.2,
                'type': 'Mid-Range Hotel',
                'location': 'Business District',
                'amenities': ['WiFi', 'Room Service', 'Breakfast', 'Gym', 'Parking'],
                'check_in': '14:00',
                'check_out': '11:00',
                'cancellation': 'Free cancellation up to 24 hours',
                'pros': ['Comfortable', 'Good facilities', 'Value for money', 'Professional service'],
                'cons': ['Less character', 'Generic feeling']
            }
        ]
    
    def _get_luxury_hotels(self, destination: str, daily_budget: float) -> List[Dict[str, Any]]:
        """
        Get luxury hotel recommendations
        
        Args:
            destination: Destination
            daily_budget: Daily budget
            
        Returns:
            List of luxury hotels
        """
        return [
            {
                'name': f'{destination} Grand Palace',
                'price_per_night': round(daily_budget * 2.5, 2),
                'rating': 4.8,
                'type': 'Luxury Hotel',
                'location': 'Premium District',
                'amenities': ['WiFi', 'Fine Dining', 'Spa', 'Gym', 'Pool', 'Concierge', 'Business Center'],
                'check_in': '14:00',
                'check_out': '12:00',
                'cancellation': 'Free cancellation up to 72 hours',
                'pros': ['Excellent service', 'Premium amenities', 'Beautiful rooms', 'Multiple restaurants'],
                'cons': ['Very expensive', 'May be formal']
            },
            {
                'name': f'{destination} Royal Resort',
                'price_per_night': round(daily_budget * 2.2, 2),
                'rating': 4.7,
                'type': 'Resort',
                'location': 'Scenic Area',
                'amenities': ['WiFi', 'Multiple Pools', 'Multiple Restaurants', 'Spa', 'Beach', 'Water Sports'],
                'check_in': '14:00',
                'check_out': '11:00',
                'cancellation': 'Free cancellation up to 72 hours',
                'pros': ['All-inclusive options', 'Great for families', 'Lots of activities'],
                'cons': ['Can feel isolated', 'Expensive']
            }
        ]

    def _enhance_luxury_list(self, destination: str, luxury_list: List[Dict[str, Any]], daily_budget: float) -> List[Dict[str, Any]]:
        """Insert famous worldwide luxury hotels when applicable (e.g., Lake Palace, Raffles)."""
        d = destination.lower()
        extras = []
        if 'udaipur' in d:
            extras.append({
                'name': 'Taj Lake Palace (Udaipur)',
                'price_per_night': round(daily_budget * 5.0, 2),
                'rating': 4.9,
                'type': 'Palace Hotel',
                'location': 'Lake Pichola',
                'amenities': ['Private boat access', 'Fine Dining', 'Spa', 'Pool', 'Butler Service'],
                'check_in': '14:00',
                'check_out': '12:00',
                'cancellation': 'Limited cancellation',
                'pros': ['Iconic location', 'Historic palace', 'Unmatched views'],
                'cons': ['Very expensive', 'Limited availability']
            })
        if 'singapore' in d:
            extras.append({
                'name': 'Raffles Hotel Singapore',
                'price_per_night': round(daily_budget * 6.0, 2),
                'rating': 4.8,
                'type': 'Colonial Luxury Hotel',
                'location': 'City Center',
                'amenities': ['Heritage suites', 'Fine Dining', 'Spa', 'Concierge'],
                'check_in': '15:00',
                'check_out': '12:00',
                'cancellation': 'Free cancellation up to 72 hours',
                'pros': ['Historic charm', 'High service standards'],
                'cons': ['Expensive']
            })

        # Always return extras first so they appear as highlighted recommendations
        return extras + luxury_list
    
    def _get_booking_tips(self) -> List[str]:
        """Get hotel booking tips"""
        return [
            'Book 2-3 weeks in advance for better rates',
            'Compare prices on multiple booking sites',
            'Check cancellation policies before booking',
            'Read recent guest reviews thoroughly',
            'Look for early-bird discounts',
            'Book directly with hotel for loyalty benefits',
            'Check for seasonal promotions',
            'Verify included amenities (breakfast, WiFi, parking)',
            'Check location on map before booking',
            'Call hotel to negotiate for longer stays'
        ]
    
    def _get_amenities_by_type(self, travel_type: str) -> Dict[str, list]:
        """
        Get recommended amenities based on travel type
        
        Args:
            travel_type: Type of travel
            
        Returns:
            Recommended amenities
        """
        base_amenities = ['WiFi', 'Air Conditioning', '24/7 Rooms Service']
        
        if travel_type == 'Family':
            return {
                'essential': base_amenities + ['Swimming Pool', 'Kids Activities', 'Family Rooms'],
                'nice_to_have': ['Game Room', 'Babysitting Service', 'Multiple Restaurants']
            }
        elif travel_type == 'Couple':
            return {
                'essential': base_amenities + ['Romantic Setting', 'Good Restaurant', 'Spa'],
                'nice_to_have': ['Sunset Views', 'Wine Selection', 'Room Service']
            }
        elif travel_type == 'Solo':
            return {
                'essential': base_amenities + ['Safe Location', 'Social Areas', 'Tour Desk'],
                'nice_to_have': ['Communal Kitchen', 'Social Events', 'Good Bars']
            }
        else:  # Friends
            return {
                'essential': base_amenities + ['Group Rates', 'Common Areas', 'Tour Desk'],
                'nice_to_have': ['Kitchen Access', 'Party Facilities', 'Activities']
            }
    
    def _get_location_recommendations(self, destination: str) -> Dict[str, Dict]:
        """
        Get location recommendations within destination
        
        Args:
            destination: Destination name
            
        Returns:
            Location information
        """
        return {
            'city_center': {
                'description': 'Heart of the city',
                'advantages': ['Close to attractions', 'Good restaurants', 'Shopping', 'Nightlife'],
                'disadvantages': ['Can be noisy', 'Expensive', 'Crowded'],
                'best_for': 'City exploration'
            },
            'near_station': {
                'description': 'Near railway/bus station',
                'advantages': ['Easy transportation', 'Budget hotels', 'Open late shops'],
                'disadvantages': ['Can be noisy', 'Less scenic', 'Safety concerns'],
                'best_for': 'Quick visits'
            },
            'scenic_area': {
                'description': 'Scenic locations',
                'advantages': ['Beautiful views', 'Peaceful', 'Good for relaxation'],
                'disadvantages': ['Far from center', 'Limited transportation', 'Fewer amenities'],
                'best_for': 'Leisure travel'
            }
        }
