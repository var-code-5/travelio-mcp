from typing import List, Dict, Optional, Any
from datetime import datetime, date
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.db.session import get_db
from app.db.models.itinerary import Itinerary, ItineraryDay, ItineraryActivity
from app.db.models.destination import Destination
from app.db.models.hotel import Hotel
from app.db.models.attraction import Attraction

class ItineraryService:
    """Service for itinerary-related operations."""
    
    async def save_itinerary(self, itinerary_data: Dict) -> int:
        """
        Save an itinerary to the database.
        
        Args:
            itinerary_data: Itinerary data to save
            
        Returns:
            ID of the saved itinerary
        """
        async with AsyncSession(next(get_db())) as session:
            # Create itinerary object
            itinerary = Itinerary(
                title=itinerary_data["title"],
                description=itinerary_data.get("description"),
                user_id=itinerary_data.get("user_id"),
                destination_id=itinerary_data["destination_id"],
                start_date=datetime.strptime(itinerary_data["start_date"], "%Y-%m-%d").date(),
                end_date=datetime.strptime(itinerary_data["end_date"], "%Y-%m-%d").date(),
                hotel_id=itinerary_data.get("hotel_id"),
                is_recommended=itinerary_data.get("is_recommended", False)
            )
            
            session.add(itinerary)
            await session.flush()
            
            # Add days
            for day_data in itinerary_data["days"]:
                day = ItineraryDay(
                    itinerary_id=itinerary.id,
                    day_number=day_data["day_number"],
                    date=datetime.strptime(day_data["date"], "%Y-%m-%d").date(),
                    hotel_id=day_data.get("hotel_id", itinerary_data.get("hotel_id"))
                )
                
                session.add(day)
                await session.flush()
                
                # Add activities
                for activity_data in day_data["activities"]:
                    activity = ItineraryActivity(
                        day_id=day.id,
                        start_time=datetime.strptime(activity_data["start_time"], "%H:%M").time(),
                        end_time=datetime.strptime(activity_data["end_time"], "%H:%M").time(),
                        activity_type=activity_data["activity_type"],
                        attraction_id=activity_data.get("attraction_id"),
                        title=activity_data["title"],
                        description=activity_data.get("description"),
                        start_location=json.dumps(activity_data.get("start_location", {})),
                        end_location=json.dumps(activity_data.get("end_location", {})),
                        travel_mode=activity_data.get("travel_mode"),
                        travel_duration_minutes=activity_data.get("travel_duration_minutes", 0),
                        notes=activity_data.get("notes")
                    )
                    
                    session.add(activity)
            
            await session.commit()
            return itinerary.id
    
    async def get_itinerary(self, itinerary_id: int) -> Dict:
        """
        Get an itinerary by ID with all related data.
        
        Args:
            itinerary_id: ID of the itinerary
            
        Returns:
            Itinerary as a dictionary
        """
        async with AsyncSession(next(get_db())) as session:
            # Query itinerary with relationships
            query = (
                select(Itinerary)
                .options(
                    joinedload(Itinerary.destination),
                    joinedload(Itinerary.hotel),
                    joinedload(Itinerary.days)
                    .joinedload(ItineraryDay.hotel),
                    joinedload(Itinerary.days)
                    .joinedload(ItineraryDay.activities)
                    .joinedload(ItineraryActivity.attraction)
                )
                .filter(Itinerary.id == itinerary_id)
            )
            
            result = await session.execute(query)
            itinerary = result.scalars().first()
            
            if not itinerary:
                raise ValueError(f"Itinerary with ID {itinerary_id} not found")
            
            # Build response dictionary
            itinerary_dict = {
                "id": itinerary.id,
                "title": itinerary.title,
                "description": itinerary.description,
                "user_id": itinerary.user_id,
                "destination": {
                    "id": itinerary.destination.id,
                    "name": itinerary.destination.name,
                    "country": itinerary.destination.country
                },
                "start_date": itinerary.start_date.isoformat(),
                "end_date": itinerary.end_date.isoformat(),
                "hotel": self._format_hotel(itinerary.hotel) if itinerary.hotel else None,
                "is_recommended": itinerary.is_recommended,
                "created_at": itinerary.created_at.isoformat(),
                "updated_at": itinerary.updated_at.isoformat(),
                "days": []
            }
            
            # Add days and activities
            for day in sorted(itinerary.days, key=lambda d: d.day_number):
                day_dict = {
                    "id": day.id,
                    "day_number": day.day_number,
                    "date": day.date.isoformat(),
                    "hotel": self._format_hotel(day.hotel) if day.hotel else None,
                    "activities": []
                }
                
                # Add activities
                for activity in sorted(day.activities, key=lambda a: a.start_time):
                    activity_dict = {
                        "id": activity.id,
                        "start_time": activity.start_time.isoformat(),
                        "end_time": activity.end_time.isoformat(),
                        "activity_type": activity.activity_type,
                        "title": activity.title,
                        "description": activity.description,
                        "start_location": json.loads(activity.start_location) if activity.start_location else None,
                        "end_location": json.loads(activity.end_location) if activity.end_location else None,
                        "travel_mode": activity.travel_mode,
                        "travel_duration_minutes": activity.travel_duration_minutes,
                        "notes": activity.notes
                    }
                    
                    if activity.attraction:
                        activity_dict["attraction"] = {
                            "id": activity.attraction.id,
                            "name": activity.attraction.name,
                            "category": activity.attraction.category,
                            "rating": activity.attraction.rating,
                            "image_url": activity.attraction.image_url
                        }
                    
                    day_dict["activities"].append(activity_dict)
                
                itinerary_dict["days"].append(day_dict)
            
            return itinerary_dict
    
    def _format_hotel(self, hotel: Hotel) -> Dict:
        """Format hotel object as dictionary."""
        return {
            "id": hotel.id,
            "name": hotel.name,
            "address": hotel.address,
            "latitude": hotel.latitude,
            "longitude": hotel.longitude,
            "rating": hotel.rating,
            "image_url": hotel.image_url
        }
