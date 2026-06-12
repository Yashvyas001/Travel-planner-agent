"""
Configuration module for Travel Planner Agent
Handles all environment variables and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # IBM Cloud Granite Configuration
    GRANITE_API_KEY = os.getenv('IBM_API_KEY', '')
    GRANITE_URL = os.getenv('IBM_WATSON_URL', 'https://api.us-south.mms.cloud.ibm.com/mms/v1')
    GRANITE_MODEL = os.getenv('GRANITE_MODEL', 'granite-13b-chat-v2')
    
    # Weather API Configuration
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5'
    
    # Hotel Recommendation Service
    HOTEL_API_KEY = os.getenv('HOTEL_API_KEY', '')
    HOTEL_API_URL = os.getenv('HOTEL_API_URL', '')
    
    # Flask Configuration
    JSONIFY_PRETTYPRINT_REGULAR = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max size
    
    # Agent Configuration
    AGENTS_TIMEOUT = 30  # seconds
    CACHE_TIMEOUT = 3600  # 1 hour
    

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    GRANITE_API_KEY = 'test-key'
    WEATHER_API_KEY = 'test-weather-key'
    

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
