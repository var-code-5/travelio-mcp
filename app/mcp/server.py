from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import Context
from mcp.server.fastmcp import FastMCP
from app.services.destination_service import DestinationService
from app.services.attraction_service import AttractionService
from app.services.hotel_service import HotelService
from app.services.itinerary_service import ItineraryService
from app.core.clustering import AttractionClusterer
from app.core.itinerary_planner import ItineraryPlanner

# Initialize FastMCP server
mcp = FastMCP("Travelio")

# Initialize services
destination_service = DestinationService()
attraction_service = AttractionService()
hotel_service = HotelService()
itinerary_service = ItineraryService()
clusterer = AttractionClusterer()
planner = ItineraryPlanner()

@mcp.tool()
async def get_destinations(search_term: Optional[str] = None) -> List[Dict]:
    """Get all destinations or search by name.
    
    Args:
        search_term: Optional search term to filter destinations
    """
    return await destination_service.get_destinations(search_term)

@mcp.tool()
async def get_attractions(destination_id: int, filters: Dict = {}) -> List[Dict]:
    """Get attractions for a destination.
    
    Args:
        destination_id: ID of the destination
        filters: Optional filters to apply (categories, ratings, etc.)
    """
    return await attraction_service.get_attractions(destination_id, filters)

@mcp.tool()
async def get_hotels(destination_id: int, filters: Dict = {}) -> List[Dict]:
    """Get hotels in a destination area.
    
    Args:
        destination_id: ID of the destination
        filters: Optional filters to apply (price, ratings, amenities, etc.)
    """
    return await hotel_service.get_hotels(destination_id, filters)

@mcp.tool()
async def cluster_attractions(attractions: List[Dict], num_days: int) -> Dict[int, List[Dict]]:
    """Cluster attractions based on proximity for multi-day planning.
    
    Args:
        attractions: List of attraction objects
        num_days: Number of days for the trip
    """
    return clusterer.cluster_attractions(attractions, num_days)

@mcp.tool()
async def create_itinerary(
    destination_id: int,
    num_days: int,
    start_date: str,
    attractions: List[Dict] = None,
    user_id: Optional[int] = None,
    hotel_id: Optional[int] = None
) -> Dict:
    """Create a new itinerary.
    
    Args:
        destination_id: ID of the destination
        num_days: Number of days for the trip
        start_date: Start date of the trip (format: YYYY-MM-DD)
        attractions: Optional list of attractions to include
        user_id: Optional user ID
        hotel_id: Optional hotel ID
    """
    # If no attractions provided, get top attractions
    if not attractions:
        attractions = await attraction_service.get_top_attractions(destination_id, num_days * 3)
    
    # Cluster attractions by day
    clustered_attractions = clusterer.cluster_attractions(attractions, num_days)
    
    # Find optimal hotel if not specified
    if not hotel_id:
        optimal_location = clusterer.find_central_point(attractions)
        hotels = await hotel_service.get_hotels_near_point(
            destination_id, 
            optimal_location["latitude"], 
            optimal_location["longitude"]
        )
        if hotels:
            hotel_id = hotels[0]["id"]
    
    # Generate the itinerary
    itinerary = planner.create_itinerary(
        destination_id=destination_id,
        start_date=start_date,
        num_days=num_days,
        clustered_attractions=clustered_attractions,
        hotel_id=hotel_id,
        user_id=user_id
    )
    
    # Save to database
    itinerary_id = await itinerary_service.save_itinerary(itinerary)
    itinerary["id"] = itinerary_id
    
    return itinerary

@mcp.tool()
async def get_itinerary(itinerary_id: int) -> Dict:
    """Get an existing itinerary by ID.
    
    Args:
        itinerary_id: ID of the itinerary to retrieve
    """
    return await itinerary_service.get_itinerary(itinerary_id)

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')

