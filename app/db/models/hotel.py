from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Hotel(Base):
    """Hotel accommodations model."""
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    destination_id = Column(Integer, ForeignKey("destination.id"), nullable=False)
    address = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_url = Column(String(255), nullable=True)
    rating = Column(Float, default=0.0, nullable=False)  # From 0 to 5
    price_per_night = Column(Float, nullable=False)
    amenities = Column(JSON, nullable=True)  # JSON array of amenities
    has_restaurant = Column(Boolean, default=False, nullable=False)
    has_pool = Column(Boolean, default=False, nullable=False)
    has_spa = Column(Boolean, default=False, nullable=False)
    has_gym = Column(Boolean, default=False, nullable=False)
    has_free_wifi = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    destination = relationship("Destination", backref="hotels")