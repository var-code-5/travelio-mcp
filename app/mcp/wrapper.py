"""ASGI wrapper for FastMCP."""

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

def create_asgi_app(mcp_instance: FastMCP) -> FastAPI:
    """
    Create an ASGI compatible application from a FastMCP instance.
    
    Args:
        mcp_instance: An instance of FastMCP
        
    Returns:
        A FastAPI application or the FastMCP instance itself if ASGI-compatible
    """
    # Check if the FastMCP instance has an app attribute
    if hasattr(mcp_instance, 'app'):
        return mcp_instance.app
    
    # If FastMCP is itself a FastAPI app or has a method to get the app
    if hasattr(mcp_instance, 'get_app'):
        return mcp_instance.get_app()
    
    # If FastMCP is ASGI-compatible, return it directly
    if hasattr(mcp_instance, "__call__"):
        return mcp_instance
    
    # If we can't find a suitable ASGI app, raise an error
    raise TypeError("Cannot extract FastAPI app from FastMCP instance")
