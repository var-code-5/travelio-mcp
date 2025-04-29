from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class HotelBase(BaseModel):
    """Base Hotel schema."""
    name: str
    description: Optional[str] = None
    destination_id: int
    address: str
    latitude: float
    longitude: float
    image_url: Optional[str] = None
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    price_per_night: float = Field(ge=0.0)
    amenities: Optional[List[str]] = None
    has_restaurant: bool = False
    has_pool: bool = False
    has_spa: bool = False
    has_gym: bool = False
    has_free_wifi: bool = True


class HotelCreate(HotelBase):
    """Schema for creating a hotel."""
    pass


class HotelUpdate(BaseModel):
    """Schema for updating a hotel."""
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    image_url: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)
    price_per_night: Optional[float] = Field(default=None, ge=0.0)
    amenities: Optional[List[str]] = None
    has_restaurant: Optional[bool] = None
    has_pool: Optional[bool] = None
    has_spa: Optional[bool] = None
    has_gym: Optional[bool] = None
    has_free_wifi: Optional[bool] = None


class HotelInDBBase(HotelBase):
    """Base schema for Hotel in DB."""
    id: int

    class Config:
        orm_mode = True


class Hotel(HotelInDBBase):
    """Schema for Hotel response."""
    pass