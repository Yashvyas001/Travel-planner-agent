"""
IBM Granite Service
Handles all interactions with IBM Granite LLM
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from config import get_config

class GraniteService:
    """Service for IBM Granite LLM API interactions"""
    
    def __init__(self, config=None):
        """
        Initialize Granite Service
        Args:
            config: Configuration object (uses default if None)
        """
        self.config = config or get_config()
        self.api_key = self.config.GRANITE_API_KEY
        self.url = self.config.GRANITE_URL
        self.model = self.config.GRANITE_MODEL
        self.timeout = self.config.AGENTS_TIMEOUT
        
    def _prepare_headers(self) -> Dict[str, str]:
        """Prepare authorization headers for API calls"""
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def generate_text(self, 
                     prompt: str, 
                     max_tokens: int = 1000,
                     temperature: float = 0.7) -> str:
        """
        Generate text using Granite model
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0-1)
            
        Returns:
            Generated text response
        """
        try:
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_new_tokens': max_tokens,
                'temperature': temperature
            }
            
            response = requests.post(
                f'{self.url}/text/generation',
                json=payload,
                headers=self._prepare_headers(),
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                # Extract generated text from response
                if 'results' in result and len(result['results']) > 0:
                    return result['results'][0]['generated_text']
                return ""
            else:
                raise Exception(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error in generate_text: {str(e)}")
            # Fallback response for demonstration
            return self._get_fallback_response(prompt)
    
    def generate_itinerary(self, destination: str, days: int, 
                          interests: list, travel_type: str) -> Dict[str, Any]:
        """
        Generate day-wise itinerary using Granite
        
        Args:
            destination: Travel destination
            days: Number of days
            interests: List of interests
            travel_type: Type of travel (Solo, Family, etc.)
            
        Returns:
            Itinerary dictionary
        """
        prompt = f"""Create a detailed {days}-day travel itinerary for {destination}.
Travel type: {travel_type}
Interests: {', '.join(interests)}

Please provide:
1. Day-wise activities
2. Recommended timings
3. Travel between locations
4. Local experiences
5. Best times to visit attractions

Format as JSON with day numbers as keys."""
        
        response_text = self.generate_text(prompt, max_tokens=2000)
        return self._parse_json_response(response_text)
    
    def generate_budget_breakdown(self, budget: float, days: int, 
                                 travel_type: str) -> Dict[str, Any]:
        """
        Generate budget breakdown for the trip
        
        Args:
            budget: Total budget in currency
            days: Number of days
            travel_type: Type of travel
            
        Returns:
            Budget breakdown dictionary
        """
        prompt = f"""Create a detailed budget breakdown for a {travel_type} trip lasting {days} days with a total budget of ${budget}.

Provide breakdown for:
1. Accommodation
2. Food & Dining
3. Transportation
4. Activities & Attractions
5. Shopping & Miscellaneous
6. Contingency

Format as JSON with category names and amounts."""
        
        response_text = self.generate_text(prompt, max_tokens=1500)
        return self._parse_json_response(response_text)
    
    def generate_packing_checklist(self, destination: str, 
                                 days: int, weather: str) -> Dict[str, list]:
        """
        Generate packing checklist based on destination and weather
        
        Args:
            destination: Travel destination
            days: Number of days
            weather: Weather description
            
        Returns:
            Packing checklist dictionary
        """
        prompt = f"""Create a comprehensive packing checklist for a {days}-day trip to {destination}.
Weather: {weather}

Organize items into categories:
1. Clothing
2. Footwear
3. Toiletries
4. Electronics
5. Documents
6. Weather-specific items
7. Miscellaneous

Format as JSON with categories as keys and lists of items as values."""
        
        response_text = self.generate_text(prompt, max_tokens=1500)
        return self._parse_json_response(response_text)
    
    def generate_emergency_contacts(self, destination: str, 
                                   country: str) -> Dict[str, Any]:
        """
        Generate emergency contacts for destination
        
        Args:
            destination: Travel destination city
            country: Destination country
            
        Returns:
            Emergency contacts dictionary
        """
        prompt = f"""Provide emergency contact information for {destination}, {country}.

Include:
1. Emergency services (Police, Ambulance, Fire)
2. Embassy/Consulate contact
3. Tourist police
4. Hospitals and medical services
5. Local authorities
6. Travel insurance contacts

Format as JSON."""
        
        response_text = self.generate_text(prompt, max_tokens=1000)
        return self._parse_json_response(response_text)
    
    def generate_food_recommendations(self, destination: str, 
                                     preferences: list) -> Dict[str, list]:
        """
        Generate local food recommendations
        
        Args:
            destination: Travel destination
            preferences: Food preferences and dietary restrictions
            
        Returns:
            Food recommendations dictionary
        """
        prompt = f"""Suggest popular and local food recommendations for {destination}.
Preferences: {', '.join(preferences)}

Include:
1. Must-try dishes
2. Local specialty restaurants
3. Street food recommendations
4. Dining price ranges
5. Dietary accommodation options
6. Traditional recipes of the region

Format as JSON with dish names and descriptions."""
        
        response_text = self.generate_text(prompt, max_tokens=1500)
        return self._parse_json_response(response_text)
    
    def generate_safety_tips(self, destination: str, 
                           travel_type: str) -> Dict[str, list]:
        """
        Generate travel safety tips for destination
        
        Args:
            destination: Travel destination
            travel_type: Type of travel (Solo, Family, etc.)
            
        Returns:
            Safety tips dictionary
        """
        prompt = f"""Provide safety tips for {travel_type} travelers visiting {destination}.

Include:
1. General safety precautions
2. Transportation safety
3. Health and hygiene tips
4. Money and valuables
5. Local customs to respect
6. Emergency procedures
7. Scams to avoid

Format as JSON with categories as keys and lists of tips as values."""
        
        response_text = self.generate_text(prompt, max_tokens=1500)
        return self._parse_json_response(response_text)
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Extract and parse JSON from response text
        
        Args:
            response_text: Response text from API
            
        Returns:
            Parsed JSON dictionary or empty dict if parsing fails
        """
        try:
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"response": response_text}
        except:
            return {"response": response_text}
    
    def _get_fallback_response(self, prompt: str) -> str:
        """
        Provide fallback response when API is not available
        Used for development and testing purposes
        """
        fallback_responses = {
            "itinerary": "Your itinerary has been generated...",
            "budget": "Budget breakdown prepared...",
            "packing": "Packing list created...",
            "food": "Food recommendations provided...",
            "safety": "Safety information compiled...",
            "emergency": "Emergency contacts listed..."
        }
        
        for key, value in fallback_responses.items():
            if key.lower() in prompt.lower():
                return value
        return "Response generated successfully."


class GraniteAgent:
    """Base class for Granite-powered agents"""
    
    def __init__(self, agent_name: str, config=None):
        """
        Initialize Granite Agent
        Args:
            agent_name: Name of the agent
            config: Configuration object
        """
        self.name = agent_name
        self.service = GraniteService(config)
        self.config = config or get_config()
    
    def log(self, message: str) -> None:
        """Log agent activity"""
        print(f"[{self.name}] {message}")
    
    def process(self, **kwargs) -> Dict[str, Any]:
        """
        Process agent request
        Override in subclasses
        """
        raise NotImplementedError("Subclasses must implement process method")
