#!/usr/bin/env python
"""
Travelio Chatbot - CLI interface for the travel planning assistant.

Usage:
  python travelio_chatbot.py

Environment variables:
  CLAUDE_API_KEY - Your Anthropic Claude API key
  MCP_SERVER_URL - URL of the MCP server (default: http://localhost:8000)
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from app.client.chatbot import TravelioChatbot

# Load environment variables
load_dotenv()

async def main():
    """Run the chatbot CLI."""
    # Get MCP server URL from environment or use default
    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    
    # Check for Claude API key
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Initialize chatbot
    print("Initializing Travelio Chatbot...")
    chatbot = TravelioChatbot(mcp_server_url)
    
    try:
        # Welcome message
        print("\n" + "="*60)
        print("    Welcome to Travelio Chatbot - Your Travel Assistant    ")
        print("="*60)
        print("\nType your questions about travel planning and destinations.")
        print("Commands:")
        print("  /reset - Reset the conversation")
        print("  /quit or /exit - Exit the chatbot")
        
        # Main conversation loop
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check exit commands
            if user_input.lower() in ["/quit", "/exit"]:
                break
            
            # Process the input
            response = await chatbot.process_command(user_input)
            
            # Print the response
            print(f"\nTravelio: {response}")
            
    finally:
        # Clean up
        await chatbot.close()
        print("\nThank you for using Travelio Chatbot. Goodbye!")

if __name__ == "__main__":
    asyncio.run(main())
