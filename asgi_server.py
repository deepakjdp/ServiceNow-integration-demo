"""
ASGI Server wrapper for FastMCP on Render
This creates an ASGI application that Render can properly bind to
"""
import os
from fastmcp_server_render import mcp

# Get the ASGI application from FastMCP
# The sse_app property provides the ASGI app for SSE transport
app = mcp.sse_app

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 10000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting FastMCP ASGI server on {host}:{port}")
    print(f"📡 Transport: SSE (Server-Sent Events)")
    print(f"🔗 ServiceNow Instance: {os.getenv('SERVICENOW_INSTANCE', 'Not configured')}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

# Made with Bob
