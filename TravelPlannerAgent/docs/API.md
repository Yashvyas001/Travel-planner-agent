# 📖 API Documentation - Travel Planner Agent

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API does not require authentication. In production, implement JWT tokens.

---

## Endpoints

### 1. Health Check
Check if the API is running.

```
GET /api/health
```

**Response (200)**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-15T10:30:45.123456",
  "service": "Travel Planner Agent"
}
```

---

### 2. Generate Complete Travel Plan
Generate a comprehensive travel plan with all recommendations.

```
POST /api/plan
Content-Type: application/json
```

**Request Body**
```json
{
  "source_location": "New York",
  "destination": "Paris",
  "days": 7,
  "budget": 3000,
  "travel_type": "Couple",
  "interests": ["Food", "Art", "Historical", "Shopping"],
  "dietary_preferences": ["Vegetarian"]
}
```

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| destination | string | Yes | Travel destination city |
| days | integer | Yes | Number of days (1-30) |
| budget | float | Yes | Total budget in USD (min 100) |
| travel_type | string | Yes | Solo / Family / Friends / Couple |
| interests | array | Yes | Array of interests (min 1) |
| source_location | string | No | Where traveling from |
| dietary_preferences | array | No | Dietary restrictions |

**Response (200)**
```json
{
  "status": "success",
  "summary": {
    "destination": "Paris",
    "duration": 7,
    "total_budget": 3000,
    "travel_type": "Couple",
    "interests": ["Food", "Art", "Historical"],
    "generated_at": "2026-01-15T10:30:45.123456"
  },
  "itinerary": { ... },
  "budget": { ... },
  "accommodation": { ... },
  "weather": { ... },
  "food": { ... },
  "emergency_info": { ... }
}
```

**Error Responses**

| Status | Error | Description |
|--------|-------|-------------|
| 400 | Invalid input | Missing or invalid parameters |
| 400 | Missing required fields | Required field not provided |
| 500 | Internal server error | Server processing error |

---

### 3. Get Itinerary Only
Get just the itinerary recommendations.

```
POST /api/itinerary
Content-Type: application/json
```

**Request Body**
```json
{
  "destination": "London",
  "days": 5,
  "interests": ["Historical", "Art"],
  "travel_type": "Solo"
}
```

**Response (200)**
```json
{
  "destination": "London",
  "duration": 5,
  "travel_type": "Solo",
  "interests": ["Historical", "Art"],
  "daily_plans": [
    {
      "day": 1,
      "morning": {
        "activity": "Morning activities for day 1",
        "time": "07:00 - 12:00",
        "location": "",
        "notes": "Start the day early"
      },
      "afternoon": { ... },
      "evening": { ... },
      "meals": { ... },
      "travel_time": "30 minutes",
      "estimated_cost": "$50-100"
    },
    ...
  ],
  "highlights": [...],
  "transportation": { ... },
  "best_times": { ... }
}
```

---

### 4. Get Budget Breakdown
Get expense breakdown for the trip.

```
POST /api/budget
Content-Type: application/json
```

**Request Body**
```json
{
  "budget": 3000,
  "days": 7,
  "travel_type": "Couple",
  "destination": "Barcelona"
}
```

**Response (200)**
```json
{
  "total_budget": 3000,
  "duration": 7,
  "travel_type": "Couple",
  "destination": "Barcelona",
  "daily_budget": 428.57,
  "breakdown": {
    "accommodation": {
      "percentage": 35,
      "amount": 1050,
      "description": "Hotels, hostels, or homestays",
      "tips": "Book in advance"
    },
    "food": {
      "percentage": 25,
      "amount": 750,
      "description": "Meals and dining",
      "tips": "Mix restaurants and street food"
    },
    ...
  },
  "money_saving_tips": [
    "Use public transportation",
    "Eat at local markets",
    ...
  ],
  "budget_alerts": [
    "✓ Good budget for comfortable travel",
    "💡 Don't forget travel insurance"
  ]
}
```

---

### 5. Get Hotel Recommendations
Get hotel suggestions based on budget.

```
POST /api/hotels
Content-Type: application/json
```

**Request Body**
```json
{
  "destination": "Tokyo",
  "budget": 3000,
  "travel_type": "Family",
  "days": 5
}
```

**Response (200)**
```json
{
  "destination": "Tokyo",
  "budget_allocation": 1050,
  "daily_hotel_budget": 210,
  "travel_type": "Family",
  "budget_hotels": [
    {
      "name": "Tokyo Budget Inn",
      "price_per_night": 147,
      "rating": 3.8,
      "type": "Budget Hotel",
      "location": "City Center",
      "amenities": ["WiFi", "Air Conditioning", "Breakfast"],
      "check_in": "14:00",
      "check_out": "11:00",
      "cancellation": "Free cancellation up to 24 hours",
      "pros": [...],
      "cons": [...]
    },
    ...
  ],
  "mid_range_hotels": [...],
  "luxury_hotels": [...],
  "booking_tips": [...],
  "amenities_guide": { ... },
  "location_recommendations": { ... }
}
```

---

### 6. Get Weather Information
Get weather forecast and recommendations.

```
POST /api/weather
Content-Type: application/json
```

**Request Body**
```json
{
  "destination": "Dubai",
  "travel_dates": "2026-03-15 to 2026-03-22"
}
```

**Response (200)**
```json
{
  "destination": "Dubai",
  "travel_dates": "2026-03-15 to 2026-03-22",
  "current_weather": {
    "city": "Dubai",
    "country": "AE",
    "temperature": 28,
    "feels_like": 30,
    "humidity": 65,
    "pressure": 1013,
    "weather": "Sunny",
    "description": "clear sky",
    "wind_speed": 5,
    "cloudiness": 10,
    "visibility": 10000
  },
  "suitability": {
    "score": 85,
    "rating": "Excellent",
    "recommendations": [
      "Perfect weather for outdoor activities",
      "High UV - Use sunscreen"
    ]
  },
  "clothing_suggestions": {
    "essentials": ["Light jacket", "Sunglasses"],
    "clothing": ["T-shirts", "Shorts"],
    "accessories": ["Hat", "Sunscreen"],
    "footwear": ["Sandals"]
  },
  "weather_alerts": [
    "☀️ High UV - use sunscreen",
    "🌡️ Very hot weather - stay hydrated"
  ],
  "health_precautions": { ... },
  "photography_tips": { ... }
}
```

---

### 7. Get Food Recommendations
Get local cuisine and dining suggestions.

```
POST /api/food
Content-Type: application/json
```

**Request Body**
```json
{
  "destination": "Bangkok",
  "preferences": ["Spicy", "Vegetarian"],
  "budget": 40,
  "travel_type": "Friends"
}
```

**Response (200)**
```json
{
  "destination": "Bangkok",
  "daily_budget": 40,
  "cuisine_preferences": ["Spicy", "Vegetarian"],
  "travel_type": "Friends",
  "must_try_dishes": [
    {
      "name": "Pad Thai",
      "description": "Stir-fried noodles with tofu and veggies",
      "best_place": "Street vendors",
      "price_range": "$2-4",
      "vegetarian": true
    },
    ...
  ],
  "restaurant_types": {
    "street_food": [...],
    "budget_restaurants": [...],
    "mid_range": [...],
    "fine_dining": [...]
  },
  "street_food": [...],
  "dietary_options": { ... },
  "dining_etiquette": { ... },
  "food_safety_tips": [...],
  "local_markets": [...],
  "cooking_classes": [...]
}
```

---

### 8. Get Packing Checklist
Get a weather-appropriate packing checklist.

```
POST /api/packing-checklist
Content-Type: application/json
```

**Request Body**
```json
{
  "destination": "Switzerland",
  "days": 7,
  "weather": "Cold and snowy"
}
```

**Response (200)**
```json
{
  "destination": "Switzerland",
  "duration": 7,
  "weather": "Cold and snowy",
  "checklist": {
    "clothing": [
      "Heavy winter coat",
      "Thermal underwear",
      "Sweaters",
      "Winter pants"
    ],
    "footwear": [
      "Winter boots",
      "Wool socks",
      "Slip-resistant shoes"
    ],
    "accessories": [
      "Winter hat",
      "Gloves",
      "Scarf",
      "Hand warmers"
    ],
    ...
  }
}
```

---

## Request/Response Codes

### Success Codes
- **200 OK**: Request successful
- **201 Created**: Resource created

### Client Error Codes
- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Authentication required (future)
- **404 Not Found**: Endpoint not found
- **422 Unprocessable Entity**: Validation error

### Server Error Codes
- **500 Internal Server Error**: Server processing error
- **503 Service Unavailable**: Service temporarily unavailable

---

## Rate Limiting

Currently no rate limiting. In production, implement:
- 100 requests per minute per IP
- Exponential backoff for retries

---

## CORS Headers

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

---

## Example Requests

### cURL Request
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Paris",
    "days": 7,
    "budget": 3000,
    "travel_type": "Couple",
    "interests": ["Food", "Art"]
  }'
```

### JavaScript Fetch
```javascript
const response = await fetch('/api/plan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    destination: 'Paris',
    days: 7,
    budget: 3000,
    travel_type: 'Couple',
    interests: ['Food', 'Art']
  })
});
const data = await response.json();
```

### Python Requests
```python
import requests

response = requests.post('http://localhost:5000/api/plan', json={
    'destination': 'Paris',
    'days': 7,
    'budget': 3000,
    'travel_type': 'Couple',
    'interests': ['Food', 'Art']
})
data = response.json()
```

---

## Versioning

Current API Version: **v1** (Implied in URLs)

Future versions will use:
```
/api/v2/plan
/api/v2/itinerary
```

---

## Best Practices

1. **Always validate input** before sending
2. **Use appropriate HTTP methods** (GET for retrieval, POST for creation)
3. **Handle errors gracefully** with proper error messages
4. **Implement retry logic** for failed requests
5. **Cache responses** when possible
6. **Use JSON format** for all requests/responses

---

## Support

For API issues:
1. Check response status codes
2. Validate request parameters
3. Review example requests
4. Check server logs

---

**API Documentation v1.0** | Generated for IBM SkillsBuild 2026
