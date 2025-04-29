# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    PROJECT_NAME: str = "Travel Itinerary App"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    DATABASE_URI: str = os.getenv("DATABASE_URI", "sqlite:///./test.db")
    
    # Security
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"  # Change in production!
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Geographic parameters
    MAX_TRAVEL_DISTANCE_KM: float = 100.0  # Maximum distance for day trips
    DEFAULT_TRAVEL_SPEED_KMH: float = 50.0  # Average travel speed
    
    # Time parameters
    DEFAULT_VISIT_DURATION_HOURS: float = 2.0  # Default time to visit an attraction
    LUNCH_BREAK_DURATION_HOURS: float = 1.0  # Duration for lunch
    DINNER_BREAK_DURATION_HOURS: float = 1.5  # Duration for dinner
    DAY_START_HOUR: int = 9  # Default start hour for day trips
    DAY_END_HOUR: int = 21  # Default end hour for day trips
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()