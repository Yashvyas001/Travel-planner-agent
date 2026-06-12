"""
Weather Service
Handles weather API interactions
"""

import requests
from typing import Dict, Any, Optional
from config import get_config

class WeatherService:
    """Service for weather API interactions"""
    
    def __init__(self, config=None):
        """
        Initialize Weather Service
        Args:
            config: Configuration object
        """
        self.config = config or get_config()
        self.api_key = self.config.WEATHER_API_KEY
        self.base_url = self.config.WEATHER_API_URL
        self.timeout = self.config.AGENTS_TIMEOUT
    
    def get_current_weather(self, city: str, country_code: str = None) -> Dict[str, Any]:
        """
        Get current weather for a city
        
        Args:
            city: City name
            country_code: ISO country code (optional)
            
        Returns:
            Weather data dictionary
        """
        try:
            location = f"{city},{country_code}" if country_code else city
            
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(
                f'{self.base_url}/weather',
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._format_weather_response(data)
            else:
                return self._get_fallback_weather()
                
        except Exception as e:
            print(f"Error fetching weather: {str(e)}")
            return self._get_fallback_weather()
    
    def get_forecast(self, city: str, days: int = 5) -> Dict[str, Any]:
        """
        Get weather forecast for a city
        
        Args:
            city: City name
            days: Number of days forecast
            
        Returns:
            Forecast data dictionary
        """
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(
                f'{self.base_url}/forecast',
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._format_forecast_response(data)
            else:
                return self._get_fallback_forecast()
                
        except Exception as e:
            print(f"Error fetching forecast: {str(e)}")
            return self._get_fallback_forecast()
    
    def get_clothing_suggestions(self, temperature: float, 
                                weather_condition: str) -> Dict[str, list]:
        """
        Get clothing suggestions based on weather
        
        Args:
            temperature: Temperature in Celsius
            weather_condition: Weather condition (e.g., 'Clouds', 'Rain')
            
        Returns:
            Clothing suggestions dictionary
        """
        suggestions = {
            'essentials': [],
            'clothing': [],
            'accessories': [],
            'footwear': []
        }
        
        # Temperature-based suggestions
        if temperature < 0:
            suggestions['essentials'] = ['Heavy winter coat', 'Thermal underwear', 'Winter hat']
            suggestions['clothing'] = ['Sweaters', 'Long pants', 'Wool socks']
            suggestions['accessories'] = ['Scarf', 'Gloves', 'Beanie']
            suggestions['footwear'] = ['Winter boots', 'Snow boots']
        elif temperature < 10:
            suggestions['essentials'] = ['Warm jacket', 'Base layers']
            suggestions['clothing'] = ['Sweaters', 'Long pants', 'Long sleeves']
            suggestions['accessories'] = ['Light scarf', 'Light gloves']
            suggestions['footwear'] = ['Closed shoes', 'Boots']
        elif temperature < 20:
            suggestions['essentials'] = ['Light jacket', 'Hoodie']
            suggestions['clothing'] = ['T-shirts', 'Long pants', 'Light sweater']
            suggestions['accessories'] = ['Light cardigan']
            suggestions['footwear'] = ['Sneakers', 'Casual shoes']
        elif temperature < 30:
            suggestions['essentials'] = ['Light layers']
            suggestions['clothing'] = ['T-shirts', 'Shorts', 'Light pants']
            suggestions['accessories'] = ['Cap', 'Sunglasses']
            suggestions['footwear'] = ['Sandals', 'Sneakers']
        else:
            suggestions['essentials'] = ['Light, breathable clothing']
            suggestions['clothing'] = ['T-shirts', 'Shorts', 'Light dresses']
            suggestions['accessories'] = ['Hat', 'Sunglasses', 'Umbrella']
            suggestions['footwear'] = ['Sandals', 'Flip-flops']
        
        # Weather-specific suggestions
        if 'rain' in weather_condition.lower():
            suggestions['essentials'].append('Waterproof jacket')
            suggestions['accessories'].append('Umbrella')
            suggestions['footwear'].append('Waterproof shoes')
        elif 'sunny' in weather_condition.lower() or 'clear' in weather_condition.lower():
            suggestions['accessories'].append('Sunscreen lotion')
            suggestions['accessories'].append('Light sunglasses')
        elif 'snow' in weather_condition.lower():
            suggestions['essentials'].append('Winter gloves')
            suggestions['footwear'].append('Snow boots')
        
        return suggestions
    
    def _format_weather_response(self, data: Dict) -> Dict[str, Any]:
        """
        Format raw weather API response
        
        Args:
            data: Raw API response
            
        Returns:
            Formatted weather dictionary
        """
        return {
            'city': data.get('name', 'Unknown'),
            'country': data.get('sys', {}).get('country', ''),
            'temperature': data.get('main', {}).get('temp', 0),
            'feels_like': data.get('main', {}).get('feels_like', 0),
            'humidity': data.get('main', {}).get('humidity', 0),
            'pressure': data.get('main', {}).get('pressure', 0),
            'weather': data.get('weather', [{}])[0].get('main', 'Unknown'),
            'description': data.get('weather', [{}])[0].get('description', 'Unknown'),
            'wind_speed': data.get('wind', {}).get('speed', 0),
            'cloudiness': data.get('clouds', {}).get('all', 0),
            'visibility': data.get('visibility', 0)
        }
    
    def _format_forecast_response(self, data: Dict) -> Dict[str, Any]:
        """
        Format raw forecast API response
        
        Args:
            data: Raw API response
            
        Returns:
            Formatted forecast dictionary
        """
        forecasts = []
        for item in data.get('list', []):
            forecasts.append({
                'datetime': item.get('dt_txt', ''),
                'temperature': item.get('main', {}).get('temp', 0),
                'weather': item.get('weather', [{}])[0].get('main', 'Unknown'),
                'description': item.get('weather', [{}])[0].get('description', 'Unknown'),
                'humidity': item.get('main', {}).get('humidity', 0),
                'wind_speed': item.get('wind', {}).get('speed', 0)
            })
        
        return {
            'city': data.get('city', {}).get('name', 'Unknown'),
            'forecasts': forecasts
        }
    
    def _get_fallback_weather(self) -> Dict[str, Any]:
        """
        Provide fallback weather data for development
        """
        return {
            'city': 'Default City',
            'country': 'Fallback',
            'temperature': 25,
            'feels_like': 26,
            'humidity': 65,
            'pressure': 1013,
            'weather': 'Partly Cloudy',
            'description': 'partly cloudy',
            'wind_speed': 5,
            'cloudiness': 40,
            'visibility': 10000
        }
    
    def _get_fallback_forecast(self) -> Dict[str, Any]:
        """
        Provide fallback forecast data for development
        """
        return {
            'city': 'Default City',
            'forecasts': [
                {
                    'datetime': '2024-01-01 12:00:00',
                    'temperature': 25,
                    'weather': 'Sunny',
                    'description': 'clear sky',
                    'humidity': 60,
                    'wind_speed': 5
                }
            ]
        }


class TravelWeatherAnalyzer:
    """Analyze weather for travel suitability"""
    
    def __init__(self, config=None):
        """Initialize analyzer"""
        self.weather_service = WeatherService(config)
    
    def analyze_travel_weather(self, destination: str, travel_dates: str) -> Dict[str, Any]:
        """
        Analyze if weather is suitable for travel
        
        Args:
            destination: Travel destination
            travel_dates: Travel date range
            
        Returns:
            Analysis dictionary with recommendations
        """
        weather = self.weather_service.get_current_weather(destination)
        forecast = self.weather_service.get_forecast(destination)
        
        suitability = self._calculate_suitability(weather, forecast)
        
        return {
            'destination': destination,
            'current_weather': weather,
            'forecast': forecast,
            'suitability_score': suitability['score'],
            'suitability_rating': suitability['rating'],
            'recommendations': suitability['recommendations'],
            'packing_suggestions': self.weather_service.get_clothing_suggestions(
                weather.get('temperature', 20),
                weather.get('weather', 'Clear')
            )
        }
    
    def _calculate_suitability(self, weather: Dict, forecast: Dict) -> Dict[str, Any]:
        """
        Calculate travel suitability score
        
        Args:
            weather: Current weather data
            forecast: Forecast data
            
        Returns:
            Suitability dictionary with score and recommendations
        """
        score = 100
        recommendations = []
        
        temp = weather.get('temperature', 20)
        
        # Temperature suitability
        if temp < 0:
            score -= 20
            recommendations.append('Very cold weather - bring proper winter gear')
        elif temp < 10:
            score -= 10
            recommendations.append('Cold weather - bring layers and warm clothing')
        elif temp > 45:
            score -= 20
            recommendations.append('Extremely hot - stay hydrated and use sun protection')
        elif temp > 35:
            score -= 10
            recommendations.append('Very hot weather - plan indoor activities during peak heat')
        
        # Weather conditions
        weather_type = weather.get('weather', 'Unknown').lower()
        if 'rain' in weather_type or 'storm' in weather_type:
            score -= 15
            recommendations.append('Rainy weather - carry umbrella and waterproof gear')
        elif 'snow' in weather_type:
            score -= 20
            recommendations.append('Snowy conditions - bring snow boots and heavy winter clothing')
        
        # Humidity
        humidity = weather.get('humidity', 50)
        if humidity > 80:
            recommendations.append('High humidity - dress lightly and stay hydrated')
        
        rating = 'Excellent' if score >= 80 else 'Good' if score >= 60 else 'Fair' if score >= 40 else 'Poor'
        
        return {
            'score': score,
            'rating': rating,
            'recommendations': recommendations
        }
