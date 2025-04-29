from typing import Optional, List
from pydantic import BaseModel, Field


class DestinationBase(BaseModel):
    """Base Destination schema."""
    name: str
    country: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    image_url: Optional[str] = None
    popularity_score: float = Field(default=0.0, ge=0.0, le=10.0)


class DestinationCreate(DestinationBase):
    """Schema for creating a destination."""
    pass


class DestinationUpdate(BaseModel):
    """Schema for updating a destination."""
    name: Optional[str] = None
    country: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    popularity_score: Optional[float] = Field(default=None, ge=0.0, le=10.0)


class DestinationInDBBase(DestinationBase):
    """Base schema for Destination in DB."""
    id: int

    class Config:
        orm_mode = True


class Destination(DestinationInDBBase):
    """Schema for Destination response."""
    pass