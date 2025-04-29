from typing import List, Dict, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_

from app.db.session import get_db
from app.db.models.attraction import Attraction

class AttractionService:
    """Service for attraction-related operations."""
    
    async def get_attractions(self, destination_id: int, filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        Get attractions for a destination with optional filters.
        
        Args:
            destination_id: ID of the destination
            filters: Optional filters like category, price_range, etc.
            
        Returns:
            List of attraction dictionaries
        """
        async with AsyncSession(next(get_db())) as session:
            query = select(Attraction).filter(Attraction.destination_id == destination_id)
            
            if filters:
                # Apply category filter if provided
                if "category" in filters:
                    categories = filters["category"] if isinstance(filters["category"], list) else [filters["category"]]
                    query = query.filter(Attraction.category.in_(categories))
                
                # Apply price range filter if provided
                if "max_price_range" in filters:
                    query = query.filter(Attraction.price_range <= filters["max_price_range"])
                
                # Apply must-visit filter if provided
                if "must_visit" in filters and filters["must_visit"]:
                    query = query.filter(Attraction.is_must_visit == True)
            
            # Order by rating (descending) and then by is_must_visit
            query = query.order_by(Attraction.is_must_visit.desc(), Attraction.rating.desc())
            
            result = await session.execute(query)
            attractions = result.scalars().all()
            
            return [
                {
                    "id": attr.id,
                    "name": attr.name,
                    "description": attr.description,
                    "destination_id": attr.destination_id,
                    "category": attr.category,
                    "latitude": attr.latitude,
                    "longitude": attr.longitude,
                    "image_url": attr.image_url,
                    "rating": attr.rating,
                    "price_range": attr.price_range,
                    "visit_duration_minutes": attr.visit_duration_minutes,
                    "opening_hours": attr.opening_hours,
                    "is_must_visit": attr.is_must_visit
                }
                for attr in attractions
            ]
    
    async def get_top_attractions(self, destination_id: int, limit: int = 10) -> List[Dict]:
        """
        Get top attractions for a destination based on rating and must-visit status.
        
        Args:
            destination_id: ID of the destination
            limit: Maximum number of attractions to return
            
        Returns:
            List of attraction dictionaries
        """
        async with AsyncSession(next(get_db())) as session:
            query = (
                select(Attraction)
                .filter(Attraction.destination_id == destination_id)
                .order_by(Attraction.is_must_visit.desc(), Attraction.rating.desc())
                .limit(limit)
            )
            
            result = await session.execute(query)
            attractions = result.scalars().all()
            
            return [
                {
                    "id": attr.id,
                    "name": attr.name,
                    "description": attr.description,
                    "destination_id": attr.destination_id,
                    "category": attr.category,
                    "latitude": attr.latitude,
                    "longitude": attr.longitude,
                    "image_url": attr.image_url,
                    "rating": attr.rating,
                    "price_range": attr.price_range,
                    "visit_duration_minutes": attr.visit_duration_minutes,
                    "opening_hours": attr.opening_hours,
                    "is_must_visit": attr.is_must_visit
                }
                for attr in attractions
            ]
