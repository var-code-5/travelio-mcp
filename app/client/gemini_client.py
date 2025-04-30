"""Gemini AI API integration for Travelio chatbot."""

import os
import httpx
import json
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self):
        """Initialize the Gemini client."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
            
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.client = httpx.AsyncClient(timeout=60.0)
        
        # Set up the system prompt for travel assistant
        self.system_prompt = """
        You are a helpful travel assistant for a service called Travelio. 
        Your job is to help users plan their trips by suggesting destinations, attractions, 
        hotels, and creating customized travel itineraries.

        Use the tools provided to fetch real data about destinations, attractions, and hotels.
        When creating itineraries, be specific about dates, attractions, and logistics.

        Always be polite, helpful, and concise in your responses. 
        If you don't know something or if the data isn't available, be honest about it.

        When users request an itinerary, make sure to get:
        1. The destination they want to visit
        2. The dates or duration of their trip
        3. Any specific attractions they want to include
        4. Any preferences (e.g., hotels, activities, budget)
        """
        
        self.conversation_history = []
        
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def send_message(self, message: str, context: Optional[Dict] = None) -> str:
        """
        Send a message to Gemini and get a response.
        
        Args:
            message: User message
            context: Optional context information about available data
            
        Returns:
            Gemini's response
        """
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "parts": [{"text": message}]})
        
        # Build the context information if provided
        context_str = ""
        if context:
            context_str = "Available data:\n" + json.dumps(context, indent=2)
        
        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": self.system_prompt + ("\n\n" + context_str if context else "")}]
                }
            ] + self.conversation_history,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000,
            }
        }
        
        # Send request to Gemini API
        url = f"{self.api_url}?key={self.api_key}"
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        
        # Extract and return Gemini's response
        result = response.json()
        assistant_message = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{"text": "Sorry, I couldn't process your request."}])[0].get("text")
        
        # Add assistant response to conversation history
        self.conversation_history.append({"role": "model", "parts": [{"text": assistant_message}]})
        
        return assistant_message
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
