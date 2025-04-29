from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON, Time, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Attraction(Base):
    """Tourist attractions model."""
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    destination_id = Column(Integer, ForeignKey("destination.id"), nullable=False)
    category = Column(String(50), index=True, nullable=False)  # e.g., 'Beach', 'Temple', 'Museum'
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_url = Column(String(255), nullable=True)
    rating = Column(Float, default=0.0, nullable=False)  # From 0 to 5
    price_range = Column(Integer, default=1, nullable=False)  # 1 to 5, with 5 being most expensive
    visit_duration_minutes = Column(Integer, default=120, nullable=False)  # Estimated time to visit in minutes
    opening_hours = Column(JSON, nullable=True)  # JSON with opening hours for each day
    is_must_visit = Column(Boolean, default=False, nullable=False)  # Flag for must-visit attractions
    
    # Relationships
    destination = relationship("Destination", backref="attractions")