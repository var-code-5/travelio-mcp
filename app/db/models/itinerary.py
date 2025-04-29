from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, JSON, DateTime, Date, Time, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Itinerary(Base):
    """Itinerary model."""
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, index=True, nullable=True)  # Optional user ID for saving personal itineraries
    destination_id = Column(Integer, ForeignKey("destination.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=True)  # Optional hotel selection
    is_recommended = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    destination = relationship("Destination")
    hotel = relationship("Hotel")
    days = relationship("ItineraryDay", back_populates="itinerary", cascade="all, delete-orphan")
    
    
class ItineraryDay(Base):
    """Itinerary day model."""
    
    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itinerary.id"), nullable=False)
    day_number = Column(Integer, nullable=False)  # Day 1, Day 2, etc.
    date = Column(Date, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotel.id"), nullable=True)  # Optional different hotel for this day
    
    # Relationships
    itinerary = relationship("Itinerary", back_populates="days")
    hotel = relationship("Hotel")
    activities = relationship("ItineraryActivity", back_populates="day", cascade="all, delete-orphan")
    
    
class ItineraryActivity(Base):
    """Itinerary activity model."""
    
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("itineraryday.id"), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    activity_type = Column(String(50), nullable=False)  # 'attraction', 'transfer', 'meal', 'free_time'
    attraction_id = Column(Integer, ForeignKey("attraction.id"), nullable=True)
    title = Column(String(100), nullable=False)  # Title of activity
    description = Column(Text, nullable=True)
    start_location = Column(JSON, nullable=True)  # JSON with lat/lng
    end_location = Column(JSON, nullable=True)  # JSON with lat/lng
    travel_mode = Column(String(20), nullable=True)  # 'walking', 'driving', 'transit', etc.
    travel_duration_minutes = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    day = relationship("ItineraryDay", back_populates="activities")
    attraction = relationship("Attraction", backref="itinerary_activities")