from typing import Optional, Dict, Any, List
from datetime import time
from pydantic import BaseModel, Field


class OpeningHours(BaseModel):
    """Schema for attraction opening hours."""
    monday: Optional[Dict[str, time]] = None
    tuesday: Optional[Dict[str, time]] = None
    wednesday: Optional[Dict[str, time]] = None
    thursday: Optional[Dict[str, time]] = None
    friday: Optional[Dict[str, time]] = None
    saturday: Optional[Dict[str, time]] = None
    sunday: Optional[Dict[str, time]] = None


class AttractionBase(BaseModel):
    """Base Attraction schema."""
    name: str
    description: Optional[str] = None
    destination_id: int
    category: str
    latitude: float
    longitude: float
    image_url: Optional[str] = None
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    price_range: int = Field(default=1, ge=1, le=5)
    visit_duration_minutes: int = Field(default=120, ge=15)
    opening_hours: Optional[Dict[str, Any]] = None
    is_must_visit: bool = False


class AttractionCreate(AttractionBase):
    """Schema for creating an attraction."""
    pass


class AttractionUpdate(BaseModel):
    """Schema for updating an attraction."""
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    price_range: Optional[int] = Field(default=None, ge=1, le=5)
    visit_duration_minutes: Optional[int] = Field(default=None, ge=15)
    opening_hours: Optional[Dict[str, Any]] = None
    is_must_visit: Optional[bool] = None


class AttractionInDBBase(AttractionBase):
    """Base schema for Attraction in DB."""
    id: int

    class Config:
        orm_mode = True


class Attraction(AttractionInDBBase):
    """Schema for Attraction response."""
    pass