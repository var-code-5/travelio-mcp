# app/core/config.py
import os
import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings."""
    
    # API settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/travel_mcp")
    DATABASE_URI: Optional[str] = None

    @validator("DATABASE_URI", pre=True)
    def assemble_db_uri(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if v or not values.get("DATABASE_URL"):
            return v
        # Convert DATABASE_URL to async format if it's not already
        db_url = values.get("DATABASE_URL")
        if db_url and not db_url.startswith("postgresql+asyncpg://"):
            # Replace postgresql:// with postgresql+asyncpg://
            if db_url.startswith("postgresql://"):
                return db_url.replace("postgresql://", "postgresql+asyncpg://")
            # Or just add the prefix
            return f"postgresql+asyncpg://{db_url.split('://', 1)[1]}"
        return db_url
    
    # Travel planning settings
    DAY_START_HOUR: int = 9  # Start of day for itinerary planning
    DAY_END_HOUR: int = 21   # End of day for itinerary planning
    LUNCH_BREAK_DURATION_HOURS: float = 1.0
    DINNER_BREAK_DURATION_HOURS: float = 1.5
    DEFAULT_TRAVEL_SPEED_KMH: float = 30.0  # Average travel speed in cities
    
    # App settings
    PROJECT_NAME: str = "Travelio"
    
    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()