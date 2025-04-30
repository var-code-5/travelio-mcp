"""MCP Client for Travelio."""

from typing import Dict, List, Any, Optional
import os
import httpx
import json
import asyncio

class TravelioMCPClient:
    """Client for connecting to Travelio MCP Server."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the MCP client.
        
        Args:
            base_url: Base URL of the MCP server
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)
        
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
        
    async def get_destinations(self, search_term: Optional[str] = None) -> List[Dict]:
        """
        Get destinations matching the search term.
        
        Args:
            search_term: Optional search term to filter destinations
            
        Returns:
            List of destination dictionaries
        """
        params = {}
        if search_term:
            params["search_term"] = search_term
            
        response = await self.client.post("/tool/get_destinations", json=params)
        response.raise_for_status()
        return response.json()
    
    async def get_attractions(self, destination_id: int, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Get attractions for a destination.
        
        Args:
            destination_id: ID of the destination
            filters: Optional filters for attractions
            
        Returns:
            List of attraction dictionaries
        """
        params = {"destination_id": destination_id}
        if filters:
            params["filters"] = filters
            
        response = await self.client.post("/tool/get_attractions", json=params)
        response.raise_for_status()
        return response.json()
    
    async def get_hotels(self, destination_id: int, filters: Optional[Dict] = None) -> List[Dict]:
        """
        Get hotels for a destination.
        
        Args:
            destination_id: ID of the destination
            filters: Optional filters for hotels
            
        Returns:
            List of hotel dictionaries
        """
        params = {"destination_id": destination_id}
        if filters:
            params["filters"] = filters
            
        response = await self.client.post("/tool/get_hotels", json=params)
        response.raise_for_status()
        return response.json()
    
    async def create_itinerary(
        self, 
        destination_id: int, 
        num_days: int, 
        start_date: str,
        attractions: Optional[List[Dict]] = None,
        user_id: Optional[int] = None,
        hotel_id: Optional[int] = None
    ) -> Dict:
        """
        Create an itinerary.
        
        Args:
            destination_id: ID of the destination
            num_days: Number of days for the itinerary
            start_date: Start date in format YYYY-MM-DD
            attractions: Optional list of attractions to include
            user_id: Optional user ID
            hotel_id: Optional hotel ID
            
        Returns:
            Itinerary dictionary
        """
        params = {
            "destination_id": destination_id,
            "num_days": num_days,
            "start_date": start_date
        }
        
        if attractions:
            params["attractions"] = attractions
        if user_id:
            params["user_id"] = user_id
        if hotel_id:
            params["hotel_id"] = hotel_id
            
        response = await self.client.post("/tool/create_itinerary", json=params)
        response.raise_for_status()
        return response.json()
    
    async def get_itinerary(self, itinerary_id: int) -> Dict:
        """
        Get an itinerary by ID.
        
        Args:
            itinerary_id: ID of the itinerary
            
        Returns:
            Itinerary dictionary
        """
        params = {"itinerary_id": itinerary_id}
        response = await self.client.post("/tool/get_itinerary", json=params)
        response.raise_for_status()
        return response.json()
