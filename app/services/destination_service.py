from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.db.session import get_db
from app.db.models.destination import Destination

class DestinationService:
    """Service for destination-related operations."""
    
    async def get_destinations(self, search_term: Optional[str] = None) -> List[Dict]:
        """
        Get all destinations or search by name/country.
        
        Args:
            search_term: Optional search term to filter destinations
            
        Returns:
            List of destination dictionaries
        """
        async with AsyncSession(next(get_db())) as session:
            query = select(Destination)
            
            if search_term:
                query = query.filter(
                    or_(
                        Destination.name.ilike(f"%{search_term}%"),
                        Destination.country.ilike(f"%{search_term}%")
                    )
                )
            
            # Order by popularity score (descending)
            query = query.order_by(Destination.popularity_score.desc())
            
            result = await session.execute(query)
            destinations = result.scalars().all()
            
            return [
                {
                    "id": dest.id,
                    "name": dest.name,
                    "country": dest.country,
                    "description": dest.description,
                    "latitude": dest.latitude,
                    "longitude": dest.longitude,
                    "image_url": dest.image_url,
                    "popularity_score": dest.popularity_score
                }
                for dest in destinations
            ]
    
    async def get_destination(self, destination_id: int) -> Dict:
        """
        Get a single destination by ID.
        
        Args:
            destination_id: ID of the destination
            
        Returns:
            Destination as a dictionary
        """
        async with AsyncSession(next(get_db())) as session:
            result = await session.execute(
                select(Destination).filter(Destination.id == destination_id)
            )
            destination = result.scalars().first()
            
            if not destination:
                raise ValueError(f"Destination with ID {destination_id} not found")
            
            return {
                "id": destination.id,
                "name": destination.name,
                "country": destination.country,
                "description": destination.description,
                "latitude": destination.latitude,
                "longitude": destination.longitude,
                "image_url": destination.image_url,
                "popularity_score": destination.popularity_score
            }
