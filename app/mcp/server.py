from typing import Dict, List
from mcp.server.fastmcp import FastMCP  # Use FastMCP instead of MCPServer
from app.services.destination_service import DestinationService
from app.services.attraction_service import AttractionService
from app.services.hotel_service import HotelService
from app.services.itinerary_service import ItineraryService
from app.core.clustering import AttractionClusterer
from app.core.itinerary_planner import ItineraryPlanner

# Create an MCP server
mcp = FastMCP("Travelio")

# Initialize services
destination_service = DestinationService()
attraction_service = AttractionService()
hotel_service = HotelService()
itinerary_service = ItineraryService()
clusterer = AttractionClusterer()
planner = ItineraryPlanner()

# Define tools
@mcp.tool()
async def get_destinations(search_term: str = None) -> List[Dict]:
    """Get all destinations or search by name."""
    return await destination_service.get_destinations(search_term)

@mcp.tool()
async def get_attractions(destination_id: str, filters: Dict = None) -> List[Dict]:
    """Get attractions for a destination."""
    if not destination_id:
        raise ValueError("destination_id is required")
    return await attraction_service.get_attractions(destination_id, filters or {})

@mcp.tool()
async def get_hotels(destination_id: str, filters: Dict = None) -> List[Dict]:
    """Get hotels in a destination area."""
    if not destination_id:
        raise ValueError("destination_id is required")
    return await hotel_service.get_hotels(destination_id, filters or {})

@mcp.tool()
async def cluster_attractions(attractions: List[Dict], num_days: int) -> Dict[int, List[Dict]]:
    """Cluster attractions based on proximity for multi-day planning."""
    if not attractions or not num_days:
        raise ValueError("attractions and num_days are required")
    return clusterer.cluster_attractions(attractions, num_days)

@mcp.tool()
async def create_itinerary(destination_id: str, num_days: int, start_date: str, attractions: List[Dict] = None, user_id: str = None, hotel_id: str = None) -> Dict:
    """Create a new itinerary."""
    if not destination_id or not num_days or not start_date:
        raise ValueError("destination_id, num_days, and start_date are required")
    
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
async def get_itinerary(itinerary_id: str) -> Dict:
    """Get an existing itinerary by ID."""
    if not itinerary_id:
        raise ValueError("itinerary_id is required")
    return await itinerary_service.get_itinerary(itinerary_id)

# Define a resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"

def create_server():
    """Create and return the FastMCP server instance."""
    return mcp
