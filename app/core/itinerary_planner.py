from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, date, time, timedelta
import json
from math import radians, sin, cos, sqrt, atan2

from app.core.config import settings

class ItineraryPlanner:
    """
    Class for creating detailed itineraries from clusters of attractions.
    """
    
    def create_itinerary(
        self,
        destination_id: int,
        start_date: str,
        num_days: int,
        clustered_attractions: Dict[int, List[Dict]],
        hotel_id: Optional[int] = None,
        user_id: Optional[int] = None
    ) -> Dict:
        """
        Create a complete itinerary based on clustered attractions.
        
        Args:
            destination_id: ID of the destination
            start_date: Start date in 'YYYY-MM-DD' format
            num_days: Number of days for the itinerary
            clustered_attractions: Dictionary mapping day index to list of attractions
            hotel_id: Optional ID of the selected hotel
            user_id: Optional user ID for saving the itinerary
            
        Returns:
            Complete itinerary dictionary
        """
        # Parse the start date
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_obj = start_date_obj + timedelta(days=num_days-1)
        
        # Create the base itinerary
        itinerary = {
            "title": f"{num_days}-Day Itinerary",
            "description": f"A {num_days}-day itinerary created for your trip",
            "user_id": user_id,
            "destination_id": destination_id,
            "start_date": start_date,
            "end_date": end_date_obj.strftime("%Y-%m-%d"),
            "hotel_id": hotel_id,
            "is_recommended": False,
            "days": []
        }
        
        # Make sure we have enough clusters
        if len(clustered_attractions) < num_days:
            # Duplicate some clusters if needed
            for i in range(len(clustered_attractions), num_days):
                cluster_idx = i % len(clustered_attractions)
                clustered_attractions[i] = clustered_attractions[cluster_idx]
        
        # Create day plans
        for day_number in range(1, num_days + 1):
            day_date = start_date_obj + timedelta(days=day_number - 1)
            cluster_idx = day_number - 1
            
            # Get attractions for this day
            day_attractions = clustered_attractions.get(cluster_idx, [])
            
            # Create the day
            day = {
                "day_number": day_number,
                "date": day_date.strftime("%Y-%m-%d"),
                "hotel_id": hotel_id,
                "activities": []
            }
            
            # Plan the day's activities
            if day_attractions:
                # Sort attractions by priority (must-visit first, then by rating)
                day_attractions = sorted(
                    day_attractions,
                    key=lambda a: (-a.get("is_must_visit", 0), -a.get("rating", 0))
                )
                
                # Create a sequence of activities
                day["activities"] = self._create_day_activities(day_attractions, day_date)
            
            itinerary["days"].append(day)
        
        return itinerary
    
    def _create_day_activities(self, attractions: List[Dict], day_date: date) -> List[Dict]:
        """
        Create a sequence of activities for a day based on attractions.
        
        Args:
            attractions: List of attractions for the day
            day_date: Date of the day
            
        Returns:
            List of activities
        """
        activities = []
        
        # Set up time parameters
        current_time = time(settings.DAY_START_HOUR, 0)
        end_time = time(settings.DAY_END_HOUR, 0)
        
        # Add breakfast at hotel
        breakfast_end_time = self._add_time(current_time, 60)  # 1 hour for breakfast
        activities.append({
            "start_time": current_time.strftime("%H:%M"),
            "end_time": breakfast_end_time.strftime("%H:%M"),
            "activity_type": "meal",
            "title": "Breakfast at hotel",
            "description": "Start your day with breakfast at your hotel",
            "travel_mode": None,
            "travel_duration_minutes": 0
        })
        
        current_time = breakfast_end_time
        current_location = None
        
        # Lunch and dinner time windows
        lunch_start = time(12, 0)
        lunch_end = time(14, 0)
        dinner_start = time(18, 0)
        dinner_end = time(20, 0)
        
        # Add attractions
        for i, attraction in enumerate(attractions):
            # Check if we need to add lunch break
            if self._is_time_in_range(current_time, lunch_start, lunch_end) and not any(
                a["activity_type"] == "meal" and "Lunch" in a["title"] for a in activities
            ):
                lunch_duration_mins = int(settings.LUNCH_BREAK_DURATION_HOURS * 60)
                lunch_end_time = self._add_time(current_time, lunch_duration_mins)
                
                activities.append({
                    "start_time": current_time.strftime("%H:%M"),
                    "end_time": lunch_end_time.strftime("%H:%M"),
                    "activity_type": "meal",
                    "title": "Lunch break",
                    "description": "Take a break for lunch",
                    "travel_mode": None,
                    "travel_duration_minutes": 0
                })
                
                current_time = lunch_end_time
            
            # Add travel time if we have a previous location
            if current_location:
                travel_duration = self._estimate_travel_time(
                    current_location["latitude"],
                    current_location["longitude"],
                    attraction["latitude"],
                    attraction["longitude"]
                )
                
                travel_end_time = self._add_time(current_time, travel_duration)
                
                # Add travel activity
                activities.append({
                    "start_time": current_time.strftime("%H:%M"),
                    "end_time": travel_end_time.strftime("%H:%M"),
                    "activity_type": "transfer",
                    "title": f"Travel to {attraction['name']}",
                    "description": f"Travel from previous location to {attraction['name']}",
                    "start_location": {
                        "latitude": current_location["latitude"],
                        "longitude": current_location["longitude"]
                    },
                    "end_location": {
                        "latitude": attraction["latitude"],
                        "longitude": attraction["longitude"]
                    },
                    "travel_mode": "auto",
                    "travel_duration_minutes": travel_duration
                })
                
                current_time = travel_end_time
            
            # Check if adding the attraction would go past the end time
            visit_duration = attraction.get("visit_duration_minutes", 120)
            attraction_end_time = self._add_time(current_time, visit_duration)
            
            if self._compare_times(attraction_end_time, end_time) > 0:
                # Would go past the end time, so stop adding attractions
                break
            
            # Add attraction visit
            activities.append({
                "start_time": current_time.strftime("%H:%M"),
                "end_time": attraction_end_time.strftime("%H:%M"),
                "activity_type": "attraction",
                "attraction_id": attraction["id"],
                "title": f"Visit {attraction['name']}",
                "description": attraction.get("description", ""),
                "start_location": {
                    "latitude": attraction["latitude"],
                    "longitude": attraction["longitude"]
                },
                "end_location": {
                    "latitude": attraction["latitude"],
                    "longitude": attraction["longitude"]
                },
                "travel_mode": None,
                "travel_duration_minutes": 0
            })
            
            current_time = attraction_end_time
            current_location = {
                "latitude": attraction["latitude"],
                "longitude": attraction["longitude"]
            }
            
            # Check if we need to add dinner break
            if self._is_time_in_range(current_time, dinner_start, dinner_end) and not any(
                a["activity_type"] == "meal" and "Dinner" in a["title"] for a in activities
            ):
                dinner_duration_mins = int(settings.DINNER_BREAK_DURATION_HOURS * 60)
                dinner_end_time = self._add_time(current_time, dinner_duration_mins)
                
                activities.append({
                    "start_time": current_time.strftime("%H:%M"),
                    "end_time": dinner_end_time.strftime("%H:%M"),
                    "activity_type": "meal",
                    "title": "Dinner",
                    "description": "Enjoy dinner at a local restaurant",
                    "travel_mode": None,
                    "travel_duration_minutes": 0
                })
                
                current_time = dinner_end_time
        
        # Add free time if there's time left
        if self._compare_times(current_time, end_time) < 0:
            activities.append({
                "start_time": current_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "activity_type": "free_time",
                "title": "Free time",
                "description": "Explore the area at your own pace or relax at your hotel",
                "travel_mode": None,
                "travel_duration_minutes": 0
            })
        
        return activities
    
    def _add_time(self, t: time, minutes: int) -> time:
        """Add minutes to a time object."""
        dt = datetime.combine(date.today(), t) + timedelta(minutes=minutes)
        return dt.time()
    
    def _compare_times(self, t1: time, t2: time) -> int:
        """Compare two time objects. Returns -1 if t1 < t2, 0 if equal, 1 if t1 > t2."""
        dt1 = datetime.combine(date.today(), t1)
        dt2 = datetime.combine(date.today(), t2)
        if dt1 < dt2:
            return -1
        elif dt1 > dt2:
            return 1
        return 0
    
    def _is_time_in_range(self, t: time, start: time, end: time) -> bool:
        """Check if a time is within a range."""
        return self._compare_times(t, start) >= 0 and self._compare_times(t, end) <= 0
    
    def _estimate_travel_time(self, lat1: float, lon1: float, lat2: float, lon2: float) -> int:
        """
        Estimate travel time between two points based on distance.
        
        Args:
            lat1: Latitude of start point
            lon1: Longitude of start point
            lat2: Latitude of end point
            lon2: Longitude of end point
            
        Returns:
            Estimated travel time in minutes
        """
        # Calculate distance using Haversine formula
        R = 6371.0  # Earth radius in kilometers
        
        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)
        
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        
        a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance_km = R * c
        
        # Use average speed to estimate travel time
        # Default is 50 km/h, so divide by 50 and multiply by 60 to get minutes
        travel_time_minutes = int((distance_km / settings.DEFAULT_TRAVEL_SPEED_KMH) * 60)
        
        # Minimum of 5 minutes travel time
        return max(5, travel_time_minutes)
