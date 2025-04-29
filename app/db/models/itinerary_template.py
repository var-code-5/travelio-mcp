from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Boolean, SmallInteger
from sqlalchemy.orm import relationship
from app.db.base import Base


class ItineraryTemplate(Base):
    """Pre-defined itinerary templates model."""
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    destination_id = Column(Integer, ForeignKey("destination.id"), nullable=False)
    num_days = Column(SmallInteger, nullable=False)  # Duration in days
    suggested_season = Column(String(50), nullable=True)  # e.g., 'Summer', 'Winter', 'Any'
    interests = Column(JSON, nullable=True)  # JSON array of targeted interests
    template_data = Column(JSON, nullable=False)  # JSON with day-by-day activities
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    destination = relationship("Destination", backref="itinerary_templates")