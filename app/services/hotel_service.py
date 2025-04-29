from typing import List, Dict, Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_, func
from math import radians, sin, cos, sqrt, atan2

from app.db.session import get_db
from app.db.models.hotel import Hotel

class HotelService:
    """Service for hotel-related operations."""
    
    async def get_hotels(self, destination_id: int, filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        """
        Get hotels for a destination with optional filters.
        
        Args:
            destination_id: ID of the destination
            filters: Optional filters like rating, price_per_night, amenities
            
        Returns:
            List of hotel dictionaries
        """
        async with AsyncSession(next(get_db())) as session:
            query = select(Hotel).filter(Hotel.destination_id == destination_id)
            
            if filters:
                # Apply rating filter if provided
                if "min_rating" in filters:
                    query = query.filter(Hotel.rating >= filters["min_rating"])
                
                # Apply price filter if provided
                if "max_price" in filters:
                    query = query.filter(Hotel.price_per_night <= filters["max_price"])
                
                # Apply amenities filters if provided
                if "has_restaurant" in filters and filters["has_restaurant"]:
                    query = query.filter(Hotel.has_restaurant == True)
                if "has_pool" in filters and filters["has_pool"]:
                    query = query.filter(Hotel.has_pool == True)
                if "has_gym" in filters and filters["has_gym"]:
                    query = query.filter(Hotel.has_gym == True)
                if "has_spa" in filters and filters["has_spa"]:
                    query = query.filter(Hotel.has_spa == True)
            
            # Order by rating (descending)
            query = query.order_by(Hotel.rating.desc())
            
            result = await session.execute(query)
            hotels = result.scalars().all()
            
            return [
                {
                    "id": hotel.id,
                    "name": hotel.name,
                    "description": hotel.description,
                    "destination_id": hotel.destination_id,
                    "address": hotel.address,
                    "latitude": hotel.latitude,
                    "longitude": hotel.longitude,
                    "image_url": hotel.image_url,
                    "rating": hotel.rating,
                    "price_per_night": hotel.price_per_night,
                    "amenities": hotel.amenities,
                    "has_restaurant": hotel.has_restaurant,
                    "has_pool": hotel.has_pool,
                    "has_spa": hotel.has_spa,
                    "has_gym": hotel.has_gym,
                    "has_free_wifi": hotel.has_free_wifi
                }
                for hotel in hotels
            ]
    
    async def get_hotels_near_point(
        self, 
        destination_id: int, 
        latitude: float, 
        longitude: float,
        max_distance_km: float = 5.0,
        limit: int = 5
    ) -> List[Dict]:
        """
        Get hotels near a specific point (useful for finding hotels near clusters of attractions).
        
        Args:
            destination_id: ID of the destination
            latitude: Latitude of the point
            longitude: Longitude of the point
            max_distance_km: Maximum distance in kilometers
            limit: Maximum number of hotels to return
            
        Returns:
            List of hotel dictionaries with distance
        """
        async with AsyncSession(next(get_db())) as session:
            # Get all hotels in the destination
            query = select(Hotel).filter(Hotel.destination_id == destination_id)
            result = await session.execute(query)
            hotels = result.scalars().all()
            
            # Calculate distances and filter
            hotels_with_distance = []
            for hotel in hotels:
                distance = self._calculate_distance(
                    lat1=latitude,
                    lon1=longitude,
                    lat2=hotel.latitude,
                    lon2=hotel.longitude
                )
                
                if distance <= max_distance_km:
                    hotels_with_distance.append({
                        "id": hotel.id,
                        "name": hotel.name,
                        "description": hotel.description,
                        "destination_id": hotel.destination_id,
                        "address": hotel.address,
                        "latitude": hotel.latitude,
                        "longitude": hotel.longitude,
                        "image_url": hotel.image_url,
                        "rating": hotel.rating,
                        "price_per_night": hotel.price_per_night,
                        "amenities": hotel.amenities,
                        "has_restaurant": hotel.has_restaurant,
                        "has_pool": hotel.has_pool,
                        "has_spa": hotel.has_spa,
                        "has_gym": hotel.has_gym,
                        "has_free_wifi": hotel.has_free_wifi,
                        "distance_km": distance
                    })
            
            # Sort by distance and limit
            hotels_with_distance.sort(key=lambda h: h["distance_km"])
            return hotels_with_distance[:limit]
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using the Haversine formula.
        
        Args:
            lat1: Latitude of point 1
            lon1: Longitude of point 1
            lat2: Latitude of point 2
            lon2: Longitude of point 2
            
        Returns:
            Distance in kilometers
        """
        # Earth radius in kilometers
        R = 6371.0
        
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)
        
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        return distance
