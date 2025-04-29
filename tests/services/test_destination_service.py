import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.destination_service import DestinationService

@pytest.mark.asyncio
async def test_get_destinations():
    """Test getting all destinations."""
    # Mock the database session
    mock_session = MagicMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    # Mock destination objects
    mock_dest1 = MagicMock()
    mock_dest1.id = 1
    mock_dest1.name = "Paris"
    mock_dest1.country = "France"
    mock_dest1.description = "City of Lights"
    mock_dest1.latitude = 48.8566
    mock_dest1.longitude = 2.3522
    mock_dest1.image_url = "paris.jpg"
    mock_dest1.popularity_score = 9.5
    
    mock_dest2 = MagicMock()
    mock_dest2.id = 2
    mock_dest2.name = "London"
    mock_dest2.country = "UK"
    mock_dest2.description = "Big Ben and more"
    mock_dest2.latitude = 51.5074
    mock_dest2.longitude = -0.1278
    mock_dest2.image_url = "london.jpg"
    mock_dest2.popularity_score = 9.0
    
    mock_scalars.all.return_value = [mock_dest1, mock_dest2]
    mock_session.execute.return_value = mock_result
    
    # Mock the get_db function
    with patch('app.services.destination_service.get_db', return_value=iter([mock_session])):
        # Call the service method
        service = DestinationService()
        destinations = await service.get_destinations()
        
        # Assert the results
        assert len(destinations) == 2
        assert destinations[0]["id"] == 1
        assert destinations[0]["name"] == "Paris"
        assert destinations[1]["id"] == 2
        assert destinations[1]["name"] == "London"

@pytest.mark.asyncio
async def test_get_destination():
    """Test getting a single destination by ID."""
    # Mock the database session
    mock_session = MagicMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    # Mock destination object
    mock_dest = MagicMock()
    mock_dest.id = 1
    mock_dest.name = "Paris"
    mock_dest.country = "France"
    mock_dest.description = "City of Lights"
    mock_dest.latitude = 48.8566
    mock_dest.longitude = 2.3522
    mock_dest.image_url = "paris.jpg"
    mock_dest.popularity_score = 9.5
    
    mock_scalars.first.return_value = mock_dest
    mock_session.execute.return_value = mock_result
    
    # Mock the get_db function
    with patch('app.services.destination_service.get_db', return_value=iter([mock_session])):
        # Call the service method
        service = DestinationService()
        destination = await service.get_destination(1)
        
        # Assert the results
        assert destination["id"] == 1
        assert destination["name"] == "Paris"
        assert destination["country"] == "France"
        assert destination["latitude"] == 48.8566

@pytest.mark.asyncio
async def test_get_destination_not_found():
    """Test getting a non-existent destination by ID."""
    # Mock the database session
    mock_session = MagicMock(spec=AsyncSession)
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    
    # Mock empty result
    mock_scalars.first.return_value = None
    mock_session.execute.return_value = mock_result
    
    # Mock the get_db function
    with patch('app.services.destination_service.get_db', return_value=iter([mock_session])):
        # Call the service method
        service = DestinationService()
        
        # Assert it raises ValueError
        with pytest.raises(ValueError, match=r"Destination with ID 999 not found"):
            await service.get_destination(999)
