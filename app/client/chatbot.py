"""Travel chatbot integrating MCP client and Claude AI."""

import asyncio
import json
from typing import Dict, List, Any, Optional
import re
from datetime import datetime, timedelta

from app.client.mcp_client import TravelioMCPClient
from app.client.gemini_client import GeminiClient

class TravelioChatbot:
    """Chatbot for Travelio travel planning."""
    
    def __init__(self, mcp_base_url: str = "http://localhost:8000"):
        """
        Initialize the chatbot.
        
        Args:
            mcp_base_url: Base URL of the MCP server
        """
        self.mcp_client = TravelioMCPClient(mcp_base_url)
        self.claude_client = GeminiClient()
        
        # State tracking
        self.current_destination = None
        self.current_attractions = None
        self.current_hotels = None
        self.current_itinerary = None
        
    async def close(self):
        """Close all clients."""
        await self.mcp_client.close()
        await self.claude_client.close()
    
    async def process_command(self, message: str) -> str:
        """
        Process user command and return response.
        
        Args:
            message: User message
            
        Returns:
            Response message
        """
        # Check for specific commands
        if message.lower().startswith("/reset"):
            self.claude_client.reset_conversation()
            self.current_destination = None
            self.current_attractions = None
            self.current_hotels = None
            self.current_itinerary = None
            return "Conversation has been reset."
        
        # Extract potential destination search
        search_match = re.search(r"(?:find|search|looking for|about)\s+([a-zA-Z\s]+)(?:\s|$)", message.lower())
        if search_match and "destination" in message.lower():
            search_term = search_match.group(1).strip()
            destinations = await self.mcp_client.get_destinations(search_term)
            if destinations:
                self.current_destination = destinations[0]
                context = {"destinations": destinations}
                return await self.claude_client.send_message(message, context)
            else:
                return f"No destinations found matching '{search_term}'."
        
        # Handle listing all destinations
        if "list" in message.lower() and "destination" in message.lower():
            try:
                # Get all destinations (empty search term returns all)
                destinations = await self.mcp_client.get_destinations()
                if destinations:
                    destination_names = [f"- {d['name']}, {d['country']}" for d in destinations]
                    return (f"Here are the available destinations:\n\n" + 
                            "\n".join(destination_names))
                else:
                    return "No destinations are currently available in our system."
            except Exception as e:
                return f"Sorry, I couldn't retrieve the destinations: {str(e)}"
        
        # Extract potential attractions search
        if self.current_destination and "attraction" in message.lower():
            destination_id = self.current_destination["id"]
            try:
                attractions = await self.mcp_client.get_attractions(destination_id)
                if attractions:
                    self.current_attractions = attractions
                    context = {
                        "destination": self.current_destination,
                        "attractions": attractions[:10]  # Limit to not overwhelm Claude
                    }
                    return await self.claude_client.send_message(message, context)
                else:
                    return f"No attractions found for {self.current_destination['name']}."
            except Exception as e:
                return f"Error retrieving attractions: {str(e)}"
        
        # Extract potential hotels search
        if self.current_destination and "hotel" in message.lower():
            destination_id = self.current_destination["id"]
            try:
                hotels = await self.mcp_client.get_hotels(destination_id)
                if hotels:
                    self.current_hotels = hotels
                    context = {
                        "destination": self.current_destination,
                        "hotels": hotels[:5]  # Limit to not overwhelm Claude
                    }
                    return await self.claude_client.send_message(message, context)
                else:
                    return f"No hotels found for {self.current_destination['name']}."
            except Exception as e:
                return f"Error retrieving hotels: {str(e)}"
        
        # Extract potential itinerary creation
        itinerary_match = re.search(r"(?:create|plan|make)(?:\s+a|\s+an)?\s+itinerary", message.lower())
        days_match = re.search(r"(\d+)\s+(?:days?|nights?)", message.lower())
        
        if itinerary_match and self.current_destination and days_match:
            # Extract parameters for itinerary
            destination_id = self.current_destination["id"]
            num_days = int(days_match.group(1))
            
            # Get start date or use tomorrow
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})", message)
            start_date = date_match.group(1) if date_match else tomorrow
            
            # Use selected attractions or get top attractions
            attractions = self.current_attractions if self.current_attractions else None
            
            # Create itinerary
            try:
                itinerary = await self.mcp_client.create_itinerary(
                    destination_id=destination_id,
                    num_days=num_days,
                    start_date=start_date,
                    attractions=attractions
                )
                
                self.current_itinerary = itinerary
                context = {"itinerary": itinerary}
                return await self.claude_client.send_message(
                    f"Here's the {num_days}-day itinerary for {self.current_destination['name']} starting on {start_date}. "
                    f"Can you format this nicely and explain the plan to the user?", 
                    context
                )
            except Exception as e:
                return f"Sorry, I couldn't create an itinerary: {str(e)}"
        
        # Default: just pass to Claude
        try:
            context = {}
            if self.current_destination:
                context["current_destination"] = self.current_destination
            if self.current_attractions:
                context["available_attractions"] = [a["name"] for a in self.current_attractions[:10]]
            if self.current_hotels:
                context["available_hotels"] = [h["name"] for h in self.current_hotels[:5]]
            if self.current_itinerary:
                context["has_itinerary"] = True
                
            return await self.claude_client.send_message(message, context if context else None)
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
