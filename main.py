import uvicorn

def main():
    """Main entry point of the application."""
    print("Starting Travelio MCP server...")
    
    # Start the server using uvicorn
    uvicorn.run(
        "app.mcp.server:create_server",  # Reference to the create_server function
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()
