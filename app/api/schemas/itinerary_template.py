from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ItineraryTemplateBase(BaseModel):
    """Base ItineraryTemplate schema."""
    title: str
    description: Optional[str] = None
    destination_id: int
    num_days: int = Field(ge=1, le=30)
    suggested_season: Optional[str] = None
    interests: Optional[List[str]] = None
    template_data: Dict[str, Any]
    is_active: bool = True


class ItineraryTemplateCreate(ItineraryTemplateBase):
    """Schema for creating an itinerary template."""
    pass


class ItineraryTemplateUpdate(BaseModel):
    """Schema for updating an itinerary template."""
    title: Optional[str] = None
    description: Optional[str] = None
    num_days: Optional[int] = Field(default=None, ge=1, le=30)
    suggested_season: Optional[str] = None
    interests: Optional[List[str]] = None
    template_data: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class ItineraryTemplateInDBBase(ItineraryTemplateBase):
    """Base schema for ItineraryTemplate in DB."""
    id: int

    class Config:
        orm_mode = True


class ItineraryTemplate(ItineraryTemplateInDBBase):
    """Schema for ItineraryTemplate response."""
    pass