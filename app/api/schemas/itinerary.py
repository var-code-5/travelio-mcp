from typing import Optional, List, Dict, Any
from datetime import date, time, datetime
from pydantic import BaseModel, Field, validator
from .hotel import Hotel
from .attraction import Attraction


class ActivityBase(BaseModel):
    """Base Activity schema."""
    start_time: time
    end_time: time
    activity_type: str
    attraction_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    start_location: Optional[Dict[str, float]] = None
    end_location: Optional[Dict[str, float]] = None
    travel_mode: Optional[str] = None
    travel_duration_minutes: Optional[int] = None
    notes: Optional[str] = None

    @validator('end_time')
    def end_time_after_start_time(cls, v, values):
        if 'start_time' in values and v < values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v


class ActivityCreate(ActivityBase):
    """Schema for creating an activity."""
    day_id: int


class ActivityUpdate(BaseModel):
    """Schema for updating an activity."""
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    activity_type: Optional[str] = None
    attraction_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    start_location: Optional[Dict[str, float]] = None
    end_location: Optional[Dict[str, float]] = None
    travel_mode: Optional[str] = None
    travel_duration_minutes: Optional[int] = None
    notes: Optional[str] = None


class Activity(ActivityBase):
    """Schema for Activity response."""
    id: int
    attraction: Optional[Attraction] = None

    class Config:
        orm_mode = True


class ItineraryDayBase(BaseModel):
    """Base ItineraryDay schema."""
    day_number: int
    date: date
    hotel_id: Optional[int] = None


class ItineraryDayCreate(ItineraryDayBase):
    """Schema for creating an itinerary day."""
    itinerary_id: int
    activities: Optional[List[ActivityCreate]] = None


class ItineraryDayUpdate(BaseModel):
    """Schema for updating an itinerary day."""
    day_number: Optional[int] = None
    date = None
    hotel_id: Optional[int] = None


class ItineraryDay(ItineraryDayBase):
    """Schema for ItineraryDay response."""
    id: int
    hotel: Optional[Hotel] = None
    activities: List[Activity] = []

    class Config:
        orm_mode = True


class ItineraryBase(BaseModel):
    """Base Itinerary schema."""
    title: str
    description: Optional[str] = None
    destination_id: int
    start_date: date
    end_date: date
    hotel_id: Optional[int] = None
    is_recommended: bool = False

    @validator('end_date')
    def end_date_after_start_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after or equal to start_date')
        return v


class ItineraryCreate(ItineraryBase):
    """Schema for creating an itinerary."""
    user_id: Optional[int] = None
    days: Optional[List[ItineraryDayCreate]] = None


class ItineraryUpdate(BaseModel):
    """Schema for updating an itinerary."""
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    hotel_id: Optional[int] = None
    is_recommended: Optional[bool] = None


class Itinerary(ItineraryBase):
    """Schema for Itinerary response."""
    id: int
    user_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    days: List[ItineraryDay] = []
    hotel: Optional[Hotel] = None

    class Config:
        orm_mode = True


class ItineraryRequest(BaseModel):
    """Schema for requesting an itinerary generation."""
    destination_id: int
    num_nights: int = Field(ge=1, le=14)
    start_date: Optional[date] = None
    interests: Optional[List[str]] = None
    preferred_hotel_rating: Optional[float] = Field(default=None, ge=1.0, le=5.0)
    max_budget_per_night: Optional[float] = None
    preferred_attractions: Optional[List[int]] = None  # IDs of attractions the user wants to include