"""
Weather Agent
Handles weather-related travel planning
"""

from typing import Dict, Any
from services.weather_service import WeatherService, TravelWeatherAnalyzer
from services.granite_service import GraniteAgent

class WeatherAgent(GraniteAgent):
    """Agent for weather-related travel planning"""
    
    def __init__(self, config=None):
        """Initialize Weather Agent"""
        super().__init__("WeatherAgent", config)
        self.weather_service = WeatherService(config)
        self.weather_analyzer = TravelWeatherAnalyzer(config)
    
    def process(self, destination: str, travel_dates: str) -> Dict[str, Any]:
        """
        Process weather information for destination
        
        Args:
            destination: Travel destination
            travel_dates: Travel date range
            
        Returns:
            Weather information dictionary
        """
        self.log(f"Analyzing weather for {destination}")
        
        # Get weather analysis
        analysis = self.weather_analyzer.analyze_travel_weather(destination, travel_dates)
        
        weather_info = {
            'destination': destination,
            'travel_dates': travel_dates,
            'current_weather': analysis.get('current_weather', {}),
            'forecast': analysis.get('forecast', {}),
            'suitability': {
                'score': analysis.get('suitability_score', 0),
                'rating': analysis.get('suitability_rating', 'Unknown'),
                'recommendations': analysis.get('recommendations', [])
            },
            'clothing_suggestions': analysis.get('packing_suggestions', {}),
            'weather_alerts': self._get_weather_alerts(analysis),
            'health_precautions': self._get_health_precautions(analysis),
            'photography_tips': self._get_photography_tips(analysis)
        }
        
        self.log("Weather analysis complete")
        return weather_info
    
    def _get_weather_alerts(self, analysis: Dict[str, Any]) -> list:
        """
        Generate weather-related alerts
        
        Args:
            analysis: Weather analysis data
            
        Returns:
            List of alerts
        """
        alerts = []
        weather = analysis.get('current_weather', {})
        
        temp = weather.get('temperature', 20)
        humidity = weather.get('humidity', 50)
        weather_type = weather.get('weather', 'Unknown').lower()
        
        # Temperature alerts
        if temp < 0:
            alerts.append('⚠️ Below freezing - Risk of ice and snow')
        elif temp > 40:
            alerts.append('🌡️ Extreme heat - Stay hydrated and limit outdoor activities')
        
        # Humidity alerts
        if humidity > 85:
            alerts.append('💧 High humidity - Dress lightly, stay hydrated')
        
        # Weather type alerts
        if 'storm' in weather_type or 'thunder' in weather_type:
            alerts.append('⛈️ Storm warning - Stay indoors during storms')
        elif 'snow' in weather_type:
            alerts.append('❄️ Snowy conditions - Wear appropriate winter gear')
        elif 'rain' in weather_type:
            alerts.append('🌧️ Rainy weather - Carry umbrella or raincoat')
        
        # UV alerts
        if 'sunny' in weather_type or 'clear' in weather_type:
            alerts.append('☀️ High UV - Use sunscreen (SPF 30+)')
        
        return alerts
    
    def _get_health_precautions(self, analysis: Dict[str, Any]) -> Dict[str, list]:
        """
        Get health precautions based on weather
        
        Args:
            analysis: Weather analysis data
            
        Returns:
            Health precautions
        """
        weather = analysis.get('current_weather', {})
        temp = weather.get('temperature', 20)
        humidity = weather.get('humidity', 50)
        
        precautions = {
            'general': [
                'Stay hydrated - drink plenty of water',
                'Get adequate sleep',
                'Wash hands regularly',
                'Keep medications with you'
            ],
            'temperature_specific': [],
            'humidity_specific': [],
            'activity_precautions': []
        }
        
        # Temperature-specific
        if temp < 10:
            precautions['temperature_specific'] = [
                'Dress in layers',
                'Keep extremities warm',
                'Avoid prolonged exposure',
                'Watch for signs of hypothermia'
            ]
        elif temp > 30:
            precautions['temperature_specific'] = [
                'Drink more water',
                'Take breaks in shade',
                'Avoid peak sun hours (12-3 PM)',
                'Wear light-colored clothing'
            ]
        
        # Humidity-specific
        if humidity > 75:
            precautions['humidity_specific'] = [
                'Drink more water',
                'Take frequent breaks',
                'Wear breathable clothing',
                'Watch for heat-related illness'
            ]
        
        # Activity precautions
        activities = [
            'Avoid strenuous activities during extreme heat',
            'Take it slow at high altitudes',
            'Acclimate to new climate gradually',
            'Avoid swimming during storms'
        ]
        precautions['activity_precautions'] = activities
        
        return precautions
    
    def _get_photography_tips(self, analysis: Dict[str, Any]) -> Dict[str, list]:
        """
        Get photography tips based on weather
        
        Args:
            analysis: Weather analysis data
            
        Returns:
            Photography tips
        """
        weather = analysis.get('current_weather', {})
        weather_type = weather.get('weather', 'Unknown').lower()
        
        tips = {
            'general': [
                'Bring weather-protective camera gear',
                'Carry extra batteries (cold drains them fast)',
                'Use microfiber cloth for lens protection',
                'Bring UV filter for lens protection'
            ],
            'weather_specific': [],
            'best_times': [
                'Golden hour (sunrise/sunset) for best light',
                'Cloudy days for soft, even lighting',
                'Avoid midday harsh shadows'
            ]
        }
        
        # Weather-specific tips
        if 'sunny' in weather_type or 'clear' in weather_type:
            tips['weather_specific'] = [
                'Use polarizing filter for sky',
                'Shoot during golden hours for warmth',
                'Watch for harsh shadows'
            ]
        elif 'rain' in weather_type:
            tips['weather_specific'] = [
                'Use waterproof camera bag',
                'Bring lens protection',
                'Look for moody, dramatic shots',
                'Photograph reflections in puddles'
            ]
        elif 'cloudy' in weather_type:
            tips['weather_specific'] = [
                'Perfect for portrait photography',
                'Soft, diffused lighting all day',
                'Increase ISO slightly',
                'Good for landscape work'
            ]
        
        return tips
