import uvicorn
from app.mcp.server import asgi_app  # Direct import to avoid circular dependency

def main():
    """Main entry point of the application."""
    print("Starting Travelio MCP server...")
    
    # Start the server using uvicorn with the FastMCP instance directly
    uvicorn.run(
        "app.mcp.server:asgi_app",  # Reference the MCP server instance
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
