"""
Sample Travel Plans - Example Outputs
Demonstrates the Travel Planner Agent capabilities
"""

# Sample 1: Paris Weekend Getaway (Couple)
SAMPLE_PARIS_COUPLE = {
    "destination": "Paris",
    "duration": 3,
    "travel_type": "Couple",
    "budget": 1500,
    "itinerary": {
        "day_1": {
            "morning": "Arrive at Paris CDG airport, check-in at hotel",
            "afternoon": "Visit Eiffel Tower and take the elevator to the top",
            "evening": "Dinner at a romantic bistro near the Seine",
            "estimated_cost": "$150-200"
        },
        "day_2": {
            "morning": "Visit Louvre Museum, see Mona Lisa",
            "afternoon": "Shopping on Champs-Élysées",
            "evening": "Seine river cruise at sunset",
            "estimated_cost": "$120-150"
        },
        "day_3": {
            "morning": "Notre-Dame Cathedral and Latin Quarter",
            "afternoon": "Café and pastry at local patisserie",
            "evening": "Departure flight",
            "estimated_cost": "$80-100"
        }
    },
    "budget_breakdown": {
        "accommodation": 450,  # 30%
        "food": 375,  # 25%
        "activities": 450,  # 30%
        "transportation": 225  # 15%
    },
    "hotels": [
        {
            "name": "Boutique Hotel Marais",
            "price_per_night": 150,
            "rating": 4.6,
            "amenities": ["WiFi", "Romantic setting", "Restaurant"]
        }
    ],
    "restaurants": [
        "Le Jules Verne (Fine Dining)",
        "Café de Flore (Classic Bistro)",
        "L'Ami Jean (Traditional)"
    ],
    "weather": {
        "temperature": 12,
        "condition": "Partly Cloudy",
        "packing": ["Light jacket", "Comfortable shoes", "Camera"]
    }
}

# Sample 2: Adventure in Bali (Solo)
SAMPLE_BALI_SOLO = {
    "destination": "Bali",
    "duration": 7,
    "travel_type": "Solo",
    "budget": 2500,
    "highlights": [
        "Mountain trekking at sunrise",
        "Hindu temples exploration",
        "Beach activities and surfing lessons",
        "Yoga and meditation classes",
        "Local market experience"
    ],
    "daily_activities": [
        {
            "day": 1,
            "activity": "Arrive Denpasar, check-in, relax at beach"
        },
        {
            "day": 2,
            "activity": "Trek Mount Batur at sunrise, visit hot springs"
        },
        {
            "day": 3,
            "activity": "Ubud Palace and Sacred Monkey Forest Sanctuary"
        },
        {
            "day": 4,
            "activity": "Tanah Lot Temple and rice terraces"
        },
        {
            "day": 5,
            "activity": "Yoga class and spa treatment"
        },
        {
            "day": 6,
            "activity": "Snorkeling and water sports"
        },
        {
            "day": 7,
            "activity": "Departure"
        }
    ],
    "budget_breakdown": {
        "accommodation": 700,
        "food": 600,
        "activities": 800,
        "transportation": 400
    },
    "local_food": [
        "Nasi Goreng (Fried Rice)",
        "Soto Ayam (Chicken Soup)",
        "Satay with Peanut Sauce",
        "Fresh Fruit Smoothie Bowls"
    ],
    "safety_tips": [
        "Use registered taxis or Grab app",
        "Avoid walking alone at night in remote areas",
        "Respect local customs and dress modestly in temples",
        "Drink bottled water only"
    ]
}

# Sample 3: Family Beach Vacation (Egypt)
SAMPLE_EGYPT_FAMILY = {
    "destination": "Hurghada",
    "duration": 5,
    "travel_type": "Family",
    "budget": 3500,
    "family_activities": [
        "Snorkeling at Red Sea",
        "Beach relaxation",
        "Desert jeep safari",
        "Water park visits",
        "Cultural experiences"
    ],
    "accommodations": [
        {
            "type": "All-Inclusive Resort",
            "features": ["Kids pool", "Entertainment", "Multiple restaurants"],
            "price_per_night": 500,
            "rating": 4.5
        }
    ],
    "restaurants": [
        {
            "name": "Beachfront Seafood",
            "cuisine": "Egyptian/International",
            "kid_friendly": True,
            "price": "$$"
        }
    ],
    "health_considerations": [
        "Sunscreen SPF 50+",
        "Anti-diarrheal medication",
        "High altitude considerations",
        "Travel insurance essential"
    ],
    "packing_list": [
        "Swimwear (multiple sets)",
        "Beach towels",
        "Water shoes",
        "Sun hat and sunglasses",
        "Lightweight clothing",
        "Medications"
    ]
}

# Sample 4: Cultural Tokyo Trip (Friends Group)
SAMPLE_TOKYO_FRIENDS = {
    "destination": "Tokyo",
    "duration": 6,
    "travel_type": "Friends",
    "budget": 4000,  # per person
    "group_activities": [
        "Karaoke in Shibuya",
        "Sushi-making class",
        "Team sports or game experiences",
        "Nightlife and bar hopping",
        "Group dining experiences"
    ],
    "districts_to_visit": [
        "Shibuya - Shopping and nightlife",
        "Asakusa - Traditional culture",
        "Harajuku - Youth culture",
        "Shinjuku - Entertainment",
        "Tsukiji - Market and fresh sushi"
    ],
    "group_friendly_hotels": [
        {
            "name": "Mitsui Garden Hotel",
            "rooms": "Multiple rooms with group rates",
            "amenities": ["Communal lounge", "Kitchen", "Laundry"]
        }
    ],
    "nightlife_spots": [
        "Roppongi - Clubs and bars",
        "Shinjuku - Variety of venues",
        "Shibuya - Trendy establishments",
        "Tsukiji - Late-night eating"
    ]
}

# Sample Output Format
SAMPLE_API_RESPONSE = {
    "status": "success",
    "summary": {
        "destination": "City Name",
        "duration": 7,
        "total_budget": 3000,
        "travel_type": "Family",
        "interests": ["Adventure", "Food", "Nature"],
        "generated_at": "2026-01-15T10:30:45.123456"
    },
    "itinerary": {
        "destination": "City Name",
        "duration": 7,
        "daily_plans": [
            {
                "day": 1,
                "morning": {"activity": "...", "time": "07:00-12:00"},
                "afternoon": {"activity": "...", "time": "12:00-17:00"},
                "evening": {"activity": "...", "time": "17:00-22:00"},
                "meals": {"breakfast": "...", "lunch": "...", "dinner": "..."}
            }
        ]
    },
    "budget": {
        "total_budget": 3000,
        "daily_budget": 428.57,
        "breakdown": {
            "accommodation": {"amount": 1050, "percentage": 35},
            "food": {"amount": 750, "percentage": 25},
            "activities": {"amount": 450, "percentage": 15},
            "transportation": {"amount": 450, "percentage": 15},
            "shopping": {"amount": 150, "percentage": 5},
            "emergency": {"amount": 150, "percentage": 5}
        }
    },
    "accommodation": {
        "budget_hotels": [
            {
                "name": "Hotel Name",
                "price_per_night": 150,
                "rating": 4.2,
                "amenities": ["WiFi", "Breakfast", "AC"]
            }
        ],
        "mid_range_hotels": [],
        "luxury_hotels": []
    },
    "weather": {
        "current_weather": {
            "temperature": 25,
            "weather": "Sunny",
            "humidity": 60
        },
        "suitability": {
            "score": 85,
            "rating": "Excellent"
        },
        "clothing_suggestions": {
            "essentials": ["Light jacket"],
            "clothing": ["T-shirts", "Shorts"],
            "footwear": ["Sandals"]
        }
    },
    "food": {
        "must_try_dishes": [
            {
                "name": "Local Dish",
                "description": "Description",
                "price_range": "$5-10",
                "vegetarian": True
            }
        ],
        "restaurant_types": {
            "street_food": [],
            "budget_restaurants": [],
            "mid_range": [],
            "fine_dining": []
        }
    }
}

if __name__ == "__main__":
    print("Sample Travel Plans for Travel Planner Agent")
    print("=" * 50)
    print("\nAvailable samples:")
    print("1. Paris Weekend Getaway (Couple) - 3 days, $1500")
    print("2. Adventure in Bali (Solo) - 7 days, $2500")
    print("3. Family Beach Vacation (Egypt) - 5 days, $3500")
    print("4. Cultural Tokyo Trip (Friends) - 6 days, $4000/person")
    print("\nYou can use these samples to understand the output format")
