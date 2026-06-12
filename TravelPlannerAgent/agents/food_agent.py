"""
Food Recommendation Agent
Suggests local food and dining options
"""

from typing import Dict, Any, List
from services.granite_service import GraniteAgent

# Built-in food database for popular Indian cities (added per user request)
FOOD_DB = {
    'delhi': {
        'budget': [
            {"name": "Sita Ram Diwan Chand", "famous_for": "Chole Bhature", "price_for_two": "₹150-200"},
            {"name": "Karim's (Old Delhi)", "famous_for": "Mughlai Mutton Korma, Kebabs", "price_for_two": "₹500-700"},
            {"name": "Paranthe Wali Gali stalls", "famous_for": "Stuffed Parathas", "price_for_two": "₹150-300"}
        ],
        'mid_range': [
            {"name": "Barbeque Nation", "famous_for": "Live Grill Buffet", "price_for_two": "₹1500-2000"},
            {"name": "Gulati Restaurant", "famous_for": "North Indian, Butter Chicken", "price_for_two": "₹1800-2200"}
        ],
        'luxury': [
            {"name": "Indian Accent (The Lodhi)", "famous_for": "Modern Indian fine dining", "price_for_two": "₹8000-12000"},
            {"name": "Bukhara (ITC Maurya)", "famous_for": "Dal Bukhara, Tandoori", "price_for_two": "₹6000-9000"}
        ]
    },
    'mumbai': {
        'budget': [
            {"name": "Bademiya", "famous_for": "Kebabs, Rolls", "price_for_two": "₹300-500"},
            {"name": "Cafe Madras", "famous_for": "South Indian", "price_for_two": "₹250-400"}
        ],
        'mid_range': [
            {"name": "Trishna", "famous_for": "Seafood, Butter Garlic Crab", "price_for_two": "₹2500-3500"},
            {"name": "Bastian", "famous_for": "Continental Seafood", "price_for_two": "₹3000-4000"}
        ],
        'luxury': [
            {"name": "Wasabi by Morimoto (Taj Mahal Palace)", "famous_for": "Japanese fine dining", "price_for_two": "₹8000-10000"},
            {"name": "Ziya (Taj Lands End)", "famous_for": "Modern Indian", "price_for_two": "₹6000-8000"}
        ]
    },
    'jaipur': {
        'budget': [
            {"name": "Laxmi Misthan Bhandar (LMB)", "famous_for": "Rajasthani Thali, Sweets", "price_for_two": "₹400-600"},
            {"name": "Rawat Mishthan Bhandar", "famous_for": "Pyaaz Kachori", "price_for_two": "₹100-200"}
        ],
        'mid_range': [
            {"name": "Suvarna Mahal (Rambagh Palace)", "famous_for": "Royal Rajasthani Thali", "price_for_two": "₹3000-4000"}
        ],
        'luxury': [
            {"name": "1135 AD (Amber Fort)", "famous_for": "Royal dining experience", "price_for_two": "₹6000-9000"}
        ]
    },
    'bangalore': {
        'budget': [
            {"name": "Vidyarthi Bhavan", "famous_for": "Masala Dosa", "price_for_two": "₹150-250"}
        ],
        'mid_range': [
            {"name": "Windmill Craftworks", "famous_for": "Microbrewery + Continental", "price_for_two": "₹2000-2500"}
        ],
        'luxury': [
            {"name": "Mynt (Taj West End)", "famous_for": "Asian fine dining", "price_for_two": "₹5000-7000"}
        ]
    },
    'goa': {
        'budget': [
            {"name": "Vinayak Family Restaurant", "famous_for": "Goan Fish Thali", "price_for_two": "₹400-600"}
        ],
        'mid_range': [
            {"name": "Gunpowder", "famous_for": "South Indian-Goan fusion", "price_for_two": "₹1200-1800"}
        ],
        'luxury': [
            {"name": "Antares Beach Club", "famous_for": "Beachside fine dining", "price_for_two": "₹4000-6000"}
        ]
    }
}

class FoodAgent(GraniteAgent):
    """Agent for food and dining recommendations"""
    
    def __init__(self, config=None):
        """Initialize Food Agent"""
        super().__init__("FoodAgent", config)
    
    def process(self, destination: str, cuisine_preferences: List[str],
               budget: float, travel_type: str) -> Dict[str, Any]:
        """
        Generate food recommendations
        
        Args:
            destination: Travel destination
            cuisine_preferences: Preferred cuisines
            budget: Daily food budget
            travel_type: Type of travel (Solo, Family, etc.)
            
        Returns:
            Food recommendations dictionary
        """
        self.log(f"Generating food recommendations for {destination}")
        self.log(f"Preferences: {cuisine_preferences}, Budget: ${budget}")
        
        # Get food recommendations from Granite
        recommendations = self.service.generate_food_recommendations(
            destination, cuisine_preferences
        )
        
        # If we have curated data for the destination, use it to enrich results
        dest_key = destination.lower().strip()
        city_data = None
        for k in FOOD_DB.keys():
            if k in dest_key:
                city_data = FOOD_DB[k]
                break

        food_info = {
            'destination': destination,
            'daily_budget': budget,
            'cuisine_preferences': cuisine_preferences,
            'travel_type': travel_type,
            'must_try_dishes': self._get_must_try_dishes(destination),
            'restaurant_types': self._get_restaurant_recommendations(destination, budget),
            'street_food': self._get_street_food_recommendations(destination),
            'dietary_options': self._get_dietary_options(destination),
            'dining_etiquette': self._get_dining_etiquette(destination),
            'food_safety_tips': self._get_food_safety_tips(),
            'local_markets': self._get_local_markets(destination),
            'cooking_classes': self._get_cooking_classes(destination)
        }

        if city_data:
            # Map curated lists into expected structures
            food_info['restaurant_types']['budget_restaurants'] = [
                {
                    'name': r['name'],
                    'type': 'Budget',
                    'location': destination,
                    'average_price': r.get('price_for_two', ''),
                    'rating': 4.3,
                    'specialties': [r.get('famous_for', '')]
                } for r in city_data.get('budget', [])
            ]

            food_info['restaurant_types']['mid_range'] = [
                {
                    'name': r['name'],
                    'type': 'Mid-Range',
                    'location': destination,
                    'average_price': r.get('price_for_two', ''),
                    'rating': 4.4,
                    'specialties': [r.get('famous_for', '')]
                } for r in city_data.get('mid_range', [])
            ]

            food_info['restaurant_types']['fine_dining'] = [
                {
                    'name': r['name'],
                    'type': 'Fine Dining',
                    'location': destination,
                    'average_price': r.get('price_for_two', ''),
                    'rating': 4.7,
                    'specialties': [r.get('famous_for', '')]
                } for r in city_data.get('luxury', [])
            ]

            # Create must_try_dishes from famous_for entries when possible
            must_try = []
            for cat in ['budget', 'mid_range', 'luxury']:
                for r in city_data.get(cat, []):
                    must_try.append({
                        'name': r.get('famous_for', r.get('name')),
                        'description': f"Famous at {r.get('name')}",
                        'best_place': r.get('name'),
                        'price_range': r.get('price_for_two', ''),
                        'vegetarian': False
                    })
            if must_try:
                food_info['must_try_dishes'] = must_try

            # Street food: include budget items that look like street vendors
            street = []
            for r in city_data.get('budget', []):
                street.append({
                    'name': r.get('name'),
                    'location': destination,
                    'price': r.get('price_for_two', ''),
                    'best_time': 'Anytime',
                    'hygiene_level': 'Varies',
                    'description': r.get('famous_for', '')
                })
            if street:
                food_info['street_food'] = street
        
        self.log("Food recommendations generated")
        return food_info
    
    def _get_must_try_dishes(self, destination: str) -> List[Dict[str, str]]:
        """
        Get must-try dishes for destination
        
        Args:
            destination: Destination name
            
        Returns:
            List of dishes to try
        """
        return [
            {
                'name': f'{destination} Specialty Dish 1',
                'description': 'A traditional local specialty',
                'best_place': 'Local market or heritage restaurant',
                'price_range': '$3-8',
                'vegetarian': False
            },
            {
                'name': f'{destination} Specialty Dish 2',
                'description': 'Popular street food item',
                'best_place': 'Street vendors near central market',
                'price_range': '$1-3',
                'vegetarian': True
            },
            {
                'name': f'{destination} Specialty Dish 3',
                'description': 'Famous dessert of the region',
                'best_place': 'Local sweet shops',
                'price_range': '$2-5',
                'vegetarian': True
            },
            {
                'name': f'{destination} Local Beverage',
                'description': 'Traditional drink of the region',
                'best_place': 'Cafes and restaurants',
                'price_range': '$1-3',
                'vegetarian': True
            }
        ]
    
    def _get_restaurant_recommendations(self, destination: str, budget: float) -> Dict[str, list]:
        """
        Get restaurant recommendations by category
        
        Args:
            destination: Destination
            budget: Daily budget
            
        Returns:
            Restaurant recommendations
        """
        return {
            'street_food': [
                {
                    'type': 'Street Vendor',
                    'location': 'Central Market',
                    'average_price': '$2-5 per item',
                    'rating': 4.4,
                    'specialties': ['Street food', 'Snacks', 'Quick bites'],
                    'hours': 'Usually 11 AM - 10 PM',
                    'payment': 'Cash only',
                    'notes': 'Authentic local experience'
                }
            ],
            'budget_restaurants': [
                {
                    'name': f'{destination} Local Eatery',
                    'type': 'Budget Restaurant',
                    'location': 'Residential area',
                    'average_price': f'${round(budget * 0.4, 2)} per meal',
                    'rating': 4.2,
                    'specialties': ['Local cuisine', 'Set meals', 'Family recipes'],
                    'hours': '12 PM - 10 PM',
                    'payment': 'Cash and cards',
                    'booking': 'Not necessary'
                }
            ],
            'mid_range': [
                {
                    'name': f'{destination} Fusion Restaurant',
                    'type': 'Mid-Range Restaurant',
                    'location': 'City center',
                    'average_price': f'${round(budget * 0.7, 2)} per meal',
                    'rating': 4.5,
                    'specialties': ['Fusion cuisine', 'International dishes', 'Wine selection'],
                    'hours': '12 PM - 11 PM',
                    'payment': 'Cash and cards',
                    'booking': 'Recommended for weekends'
                }
            ],
            'fine_dining': [
                {
                    'name': f'{destination} Fine Restaurant',
                    'type': 'Fine Dining',
                    'location': 'Premium district',
                    'average_price': f'${round(budget * 1.5, 2)} per meal',
                    'rating': 4.7,
                    'specialties': ['Gourmet cuisine', 'Chef\'s specials', 'Fine wines'],
                    'hours': '7 PM - 11 PM',
                    'payment': 'Cards preferred',
                    'booking': 'Essential'
                }
            ]
        }
    
    def _get_street_food_recommendations(self, destination: str) -> List[Dict[str, str]]:
        """
        Get street food recommendations
        
        Args:
            destination: Destination
            
        Returns:
            Street food recommendations
        """
        return [
            {
                'name': 'Popular Street Snack 1',
                'location': 'Near bus station',
                'price': '$1-2',
                'best_time': 'Evening',
                'hygiene_level': 'Good',
                'description': 'Savory fried snack that locals love'
            },
            {
                'name': 'Popular Street Snack 2',
                'location': 'Market area',
                'price': '$2-3',
                'best_time': 'Afternoon/Evening',
                'hygiene_level': 'Good',
                'description': 'Grilled items wrapped in bread'
            },
            {
                'name': 'Popular Dessert',
                'location': 'Sweet shop near market',
                'price': '$1-2',
                'best_time': 'Anytime',
                'hygiene_level': 'Excellent',
                'description': 'Sweet treat made fresh daily'
            }
        ]
    
    def _get_dietary_options(self, destination: str) -> Dict[str, Dict[str, list]]:
        """
        Get dietary options available
        
        Args:
            destination: Destination
            
        Returns:
            Dietary options
        """
        return {
            'vegetarian': {
                'availability': ['Very Good', 'Found in most restaurants'],
                'recommendations': [
                    'Vegetable curries',
                    'Paneer dishes',
                    'Lentil preparations',
                    'Vegetable breads'
                ],
                'restaurants': [f'{destination} Vegetarian Restaurant']
            },
            'vegan': {
                'availability': ['Good', 'Available in many places'],
                'recommendations': [
                    'Plant-based curries',
                    'Rice dishes',
                    'Vegetable stir-fry',
                    'Fruit smoothies'
                ],
                'restaurants': [f'{destination} Organic Cafe']
            },
            'gluten_free': {
                'availability': ['Moderate', 'Limited options'],
                'recommendations': [
                    'Rice-based dishes',
                    'Grilled meats and fish',
                    'Fresh fruits and vegetables',
                    'Corn preparations'
                ],
                'note': 'Inform restaurants about requirements'
            },
            'dairy_free': {
                'availability': ['Good', 'Many options available'],
                'recommendations': [
                    'Coconut-based curries',
                    'Oil-based dishes',
                    'Grilled preparations',
                    'Nut-based dishes'
                ]
            }
        }
    
    def _get_dining_etiquette(self, destination: str) -> Dict[str, list]:
        """
        Get dining etiquette tips
        
        Args:
            destination: Destination
            
        Returns:
            Dining etiquette
        """
        return {
            'general_tips': [
                'Respect local customs and traditions',
                'Ask before taking photographs',
                'Greet staff politely',
                'Don\'t waste food',
                'Be patient with service speed'
            ],
            'table_manners': [
                'Use utensils appropriately',
                'Don\'t start eating until served',
                'Keep conversations at moderate volume',
                'Don\'t point or gesture with utensils',
                'Clean hands before and after eating'
            ],
            'tipping_customs': [
                'Check if tipping is expected (10-15% in most places)',
                'Round up for small bills',
                'Not required at street food stalls',
                'Cash tips preferred in small restaurants'
            ],
            'dress_code': [
                'Casual for restaurants',
                'Smart casual for mid-range',
                'Formal attire for fine dining',
                'Covered shoulders for religious or traditional places'
            ]
        }
    
    def _get_food_safety_tips(self) -> list:
        """Get food safety tips"""
        return [
            'Eat at busy restaurants (high turnover = fresh food)',
            'Avoid dishes that have been kept under heat lamps',
            'Choose cooked food over raw',
            'Peel fruits yourself when possible',
            'Drink bottled or purified water only',
            'Avoid ice cubes and smoothies in some regions',
            'Eat meat that is thoroughly cooked',
            'Choose restaurants with good hygiene standards',
            'Avoid street food if you have weak stomach',
            'Carry anti-diarrheal medication'
        ]
    
    def _get_local_markets(self, destination: str) -> List[Dict[str, str]]:
        """
        Get local market recommendations
        
        Args:
            destination: Destination
            
        Returns:
            Local market information
        """
        return [
            {
                'name': f'{destination} Central Market',
                'location': 'City center',
                'best_time': 'Early morning',
                'what_to_find': 'Fresh produce, local spices, handicrafts',
                'tips': 'Arrive early for best selection',
                'experience': 'Very authentic, crowded'
            },
            {
                'name': f'{destination} Night Bazaar',
                'location': 'Commercial district',
                'best_time': 'Evening',
                'what_to_find': 'Street food, souvenirs, local goods',
                'tips': 'Great for evening strolls',
                'experience': 'Fun, crowded, lively'
            }
        ]
    
    def _get_cooking_classes(self, destination: str) -> List[Dict[str, Any]]:
        """
        Get cooking class recommendations
        
        Args:
            destination: Destination
            
        Returns:
            Cooking class information
        """
        return [
            {
                'name': f'{destination} Culinary School',
                'location': 'City center',
                'duration': '2-4 hours',
                'price': '$30-50',
                'level': 'Beginner to Intermediate',
                'includes': ['Hands-on cooking', 'Meal tasting', 'Recipe cards'],
                'highlights': 'Learn authentic recipes from local chefs'
            },
            {
                'name': 'Market Visit + Cooking',
                'location': 'Local market',
                'duration': '4-6 hours',
                'price': '$40-80',
                'level': 'All levels',
                'includes': ['Market tour', 'Cooking', 'Lunch'],
                'highlights': 'Learn ingredient selection and preparation'
            }
        ]
