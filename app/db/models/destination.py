from sqlalchemy import Column, Integer, String, Float, Text
from app.db.base import Base


class Destination(Base):
    """Destination model for regions/cities."""
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    country = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_url = Column(String(255), nullable=True)
    popularity_score = Column(Float, default=0.0, nullable=False)  # From 0 to 10