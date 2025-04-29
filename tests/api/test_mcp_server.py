import pytest
from unittest.mock import patch, MagicMock
from mcp import Context
from app.mcp.server import TravelioMCPServer

@pytest.mark.asyncio
async def test_get_destinations():
    """Test the get_destinations MCP handler."""
    # Create mock for the service
    mock_destinations = [
        {
            "id": 1, 
            "name": "Paris", 
            "country": "France",
            "latitude": 48.8566,
            "longitude": 2.3522
        }
    ]
    
    # Create a mock context
    mock_ctx = MagicMock(spec=Context)
    mock_ctx.params = {"search_term": "Paris"}
    
    # Create MCP server with mocked service
    server = TravelioMCPServer()
    
    # Mock the service method
    with patch.object(server.destination_service, 'get_destinations', 
                     return_value=mock_destinations) as mock_method:
        # Call the handler
        result = await server.get_destinations(mock_ctx)
        
        # Assert the service was called with correct params
        mock_method.assert_called_once_with("Paris")
        
        # Assert the response
        assert result == mock_destinations
        assert len(result) == 1
        assert result[0]["name"] == "Paris"

@pytest.mark.asyncio
async def test_create_itinerary():
    """Test the create_itinerary MCP handler."""
    # Mock data
    mock_attractions = [
        {
            "id": 1,
            "name": "Eiffel Tower",
            "description": "Iconic tower",
            "latitude": 48.8584,
            "longitude": 2.2945,
            "is_must_visit": True,
            "rating": 4.7,
            "visit_duration_minutes": 120
        },
        {
            "id": 2,
            "name": "Louvre Museum",
            "description": "Famous museum",
            "latitude": 48.8606,
            "longitude": 2.3376,
            "is_must_visit": True,
            "rating": 4.8,
            "visit_duration_minutes": 180
        }
    ]
    
    mock_hotels = [
        {
            "id": 1,
            "name": "Grand Hotel Paris",
            "latitude": 48.8697,
            "longitude": 2.3080,
            "rating": 4.5
        }
    ]
    
    mock_clustered_attractions = {
        0: mock_attractions
    }
    
    mock_itinerary = {
        "id": 1,
        "title": "1-Day Itinerary",
        "destination_id": 1,
        "start_date": "2023-08-01",
        "end_date": "2023-08-01",
        "days": [
            {
                "day_number": 1,
                "date": "2023-08-01",
                "activities": []
            }
        ]
    }
    
    # Create a mock context
    mock_ctx = MagicMock(spec=Context)
    mock_ctx.params = {
        "destination_id": 1,
        "num_days": 1,
        "start_date": "2023-08-01",
        "attractions": mock_attractions
    }
    
    # Create MCP server with mocked services
    server = TravelioMCPServer()
    
    # Set up mocks
    with patch.object(server.clusterer, 'cluster_attractions', return_value=mock_clustered_attractions) as mock_cluster, \
         patch.object(server.planner, 'create_itinerary', return_value=mock_itinerary) as mock_plan, \
         patch.object(server.itinerary_service, 'save_itinerary', return_value=1) as mock_save:
        
        # Call the handler
        result = await server.create_itinerary(mock_ctx)
        
        # Assert methods were called correctly
        mock_cluster.assert_called_once()
        mock_plan.assert_called_once()
        mock_save.assert_called_once()
        
        # Assert the result
        assert result["id"] == 1
        assert result["title"] == "1-Day Itinerary"
        assert len(result["days"]) == 1
