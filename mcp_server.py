"""
MCP Server with SSE Protocol for ServiceNow Operations
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import json
import asyncio
from datetime import datetime

from servicenow_client import ServiceNowClient
from config import settings


# Pydantic models for request validation
class TicketSearchRequest(BaseModel):
    query: str = Field(..., description="Search query string")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of results")


class TicketCreateRequest(BaseModel):
    short_description: str = Field(..., description="Brief description of the issue")
    description: str = Field(..., description="Detailed description")
    priority: int = Field(default=3, ge=1, le=5, description="Priority level (1-5)")
    caller_id: Optional[str] = Field(None, description="ID of the caller")
    category: Optional[str] = Field(None, description="Ticket category")


class PriorityTicketsRequest(BaseModel):
    priority: int = Field(default=1, ge=1, le=5, description="Priority level (1-5)")
    limit: int = Field(default=20, ge=1, le=100, description="Maximum number of results")


# Initialize FastAPI app
app = FastAPI(
    title="MCP Server for ServiceNow",
    description="Model Context Protocol Server with SSE for ServiceNow Operations",
    version="1.0.0"
)

# Initialize ServiceNow client
snow_client = ServiceNowClient()


@app.get("/")
async def root():
    """Root endpoint with server information"""
    return {
        "name": "MCP Server for ServiceNow",
        "version": "1.0.0",
        "protocol": "SSE (Server-Sent Events)",
        "endpoints": {
            "search": "/tickets/search",
            "create": "/tickets/create",
            "all": "/tickets/all",
            "priority": "/tickets/priority",
            "stream": "/tickets/stream"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/tickets/search")
async def search_tickets(request: TicketSearchRequest):
    """
    Search for tickets based on query
    
    Returns matching tickets from ServiceNow
    """
    try:
        tickets = snow_client.search_tickets(
            query=request.query,
            limit=request.limit
        )
        return {
            "success": True,
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tickets/create")
async def create_ticket(request: TicketCreateRequest):
    """
    Create a new incident ticket in ServiceNow
    
    Returns the created ticket details
    """
    try:
        ticket = snow_client.create_ticket(
            short_description=request.short_description,
            description=request.description,
            priority=request.priority,
            caller_id=request.caller_id,
            category=request.category
        )
        return {
            "success": True,
            "ticket": ticket
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tickets/all")
async def get_all_tickets(limit: int = 50):
    """
    Get all tickets from ServiceNow
    
    Args:
        limit: Maximum number of tickets to return (default: 50)
    """
    try:
        tickets = snow_client.get_all_tickets(limit=limit)
        return {
            "success": True,
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tickets/priority")
async def get_priority_tickets(request: PriorityTicketsRequest):
    """
    Get tickets by priority level
    
    Returns tickets matching the specified priority
    """
    try:
        tickets = snow_client.get_priority_tickets(
            priority=request.priority,
            limit=request.limit
        )
        return {
            "success": True,
            "priority": request.priority,
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tickets/{ticket_number}")
async def get_ticket(ticket_number: str):
    """
    Get a specific ticket by its number
    
    Args:
        ticket_number: Ticket number (e.g., INC0010001)
    """
    try:
        ticket = snow_client.get_ticket_by_number(ticket_number)
        if ticket is None:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        return {
            "success": True,
            "ticket": ticket
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tickets/stream/all")
async def stream_all_tickets(limit: int = 50):
    """
    Stream all tickets using SSE protocol
    
    Args:
        limit: Maximum number of tickets to stream
    """
    async def event_generator():
        try:
            # Send initial connection message
            yield {
                "event": "connected",
                "data": json.dumps({
                    "message": "Connected to MCP Server",
                    "timestamp": datetime.utcnow().isoformat()
                })
            }
            
            # Fetch tickets
            tickets = snow_client.get_all_tickets(limit=limit)
            
            # Send total count
            yield {
                "event": "count",
                "data": json.dumps({"total": len(tickets)})
            }
            
            # Stream each ticket
            for idx, ticket in enumerate(tickets):
                yield {
                    "event": "ticket",
                    "data": json.dumps({
                        "index": idx + 1,
                        "ticket": ticket
                    })
                }
                await asyncio.sleep(0.1)  # Small delay for streaming effect
            
            # Send completion message
            yield {
                "event": "complete",
                "data": json.dumps({
                    "message": "All tickets streamed",
                    "total": len(tickets)
                })
            }
            
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_generator())


@app.get("/tickets/stream/priority/{priority}")
async def stream_priority_tickets(priority: int, limit: int = 20):
    """
    Stream priority tickets using SSE protocol
    
    Args:
        priority: Priority level (1-5)
        limit: Maximum number of tickets to stream
    """
    if priority < 1 or priority > 5:
        raise HTTPException(status_code=400, detail="Priority must be between 1 and 5")
    
    async def event_generator():
        try:
            # Send initial connection message
            yield {
                "event": "connected",
                "data": json.dumps({
                    "message": f"Streaming priority {priority} tickets",
                    "timestamp": datetime.utcnow().isoformat()
                })
            }
            
            # Fetch priority tickets
            tickets = snow_client.get_priority_tickets(priority=priority, limit=limit)
            
            # Send total count
            yield {
                "event": "count",
                "data": json.dumps({"total": len(tickets), "priority": priority})
            }
            
            # Stream each ticket
            for idx, ticket in enumerate(tickets):
                yield {
                    "event": "ticket",
                    "data": json.dumps({
                        "index": idx + 1,
                        "ticket": ticket
                    })
                }
                await asyncio.sleep(0.1)
            
            # Send completion message
            yield {
                "event": "complete",
                "data": json.dumps({
                    "message": "All priority tickets streamed",
                    "total": len(tickets)
                })
            }
            
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_generator())


@app.get("/tickets/stream/search")
async def stream_search_tickets(query: str, limit: int = 10):
    """
    Stream search results using SSE protocol
    
    Args:
        query: Search query string
        limit: Maximum number of tickets to stream
    """
    async def event_generator():
        try:
            # Send initial connection message
            yield {
                "event": "connected",
                "data": json.dumps({
                    "message": f"Searching for: {query}",
                    "timestamp": datetime.utcnow().isoformat()
                })
            }
            
            # Search tickets
            tickets = snow_client.search_tickets(query=query, limit=limit)
            
            # Send total count
            yield {
                "event": "count",
                "data": json.dumps({"total": len(tickets), "query": query})
            }
            
            # Stream each ticket
            for idx, ticket in enumerate(tickets):
                yield {
                    "event": "ticket",
                    "data": json.dumps({
                        "index": idx + 1,
                        "ticket": ticket
                    })
                }
                await asyncio.sleep(0.1)
            
            # Send completion message
            yield {
                "event": "complete",
                "data": json.dumps({
                    "message": "Search complete",
                    "total": len(tickets)
                })
            }
            
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.mcp_server_host,
        port=settings.mcp_server_port,
        log_level="info"
    )

# Made with Bob
