"""
Weather Tool

Lightweight wrapper around `services.weather_service` to keep tooling
separate and provide a small stable interface for the frontend or other
helpers to call.
"""
from typing import Dict, Any
from services.weather_service import WeatherService
from config import get_config


class WeatherTool:
    """Simple wrapper exposing current weather and forecast functions."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.service = WeatherService(self.config)

    def current(self, city: str, country_code: str = None) -> Dict[str, Any]:
        """Return current weather for a city."""
        return self.service.get_current_weather(city, country_code)

    def forecast(self, city: str, days: int = 5) -> Dict[str, Any]:
        """Return forecast for next N days (aggregated)."""
        return self.service.get_forecast(city, days)


weather_tool = WeatherTool()
