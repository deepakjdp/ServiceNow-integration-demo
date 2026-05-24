"""
FastMCP Server for ServiceNow Operations with SSE Protocol
Model Context Protocol server that exposes ServiceNow operations as tools
"""
from fastmcp import FastMCP
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv

from servicenow_client import ServiceNowClient

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("ServiceNow Operations")

# Initialize ServiceNow client
snow_client = ServiceNowClient()


@mcp.tool()
def search_tickets(query: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search for ServiceNow tickets based on a query string.
    
    Searches in both short_description and description fields.
    
    Args:
        query: Search query string to find in ticket descriptions
        limit: Maximum number of tickets to return (default: 10, max: 100)
    
    Returns:
        Dictionary containing success status, count, and list of matching tickets
    
    Example:
        search_tickets("network issue", limit=5)
    """
    try:
        # Convert limit to int if it's a string
        limit = int(limit)
        
        if limit < 1 or limit > 100:
            return {
                "success": False,
                "error": "Limit must be between 1 and 100"
            }
        
        tickets = snow_client.search_tickets(query=query, limit=limit)
        return {
            "success": True,
            "count": len(tickets),
            "query": query,
            "tickets": tickets
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def create_ticket(
    short_description: str,
    description: str,
    priority: int = 3,
    caller_id: Optional[str] = None,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new incident ticket in ServiceNow.
    
    Args:
        short_description: Brief summary of the issue (required)
        description: Detailed description of the issue (required)
        priority: Priority level from 1-5 (1=Critical, 5=Planning, default: 3)
        caller_id: ServiceNow user ID of the person reporting the issue (optional)
        category: Ticket category (e.g., "hardware", "software", "network") (optional)
    
    Returns:
        Dictionary containing success status and created ticket details
    
    Example:
        create_ticket(
            short_description="Server down",
            description="Production server is not responding to requests",
            priority=1,
            category="hardware"
        )
    """
    try:
        if priority < 1 or priority > 5:
            return {
                "success": False,
                "error": "Priority must be between 1 and 5"
            }
        
        ticket = snow_client.create_ticket(
            short_description=short_description,
            description=description,
            priority=priority,
            caller_id=caller_id,
            category=category
        )
        return {
            "success": True,
            "message": f"Ticket {ticket.get('number')} created successfully",
            "ticket": ticket
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_all_tickets(limit: int = 50) -> Dict[str, Any]:
    """
    Retrieve all incident tickets from ServiceNow.
    
    Args:
        limit: Maximum number of tickets to return (default: 50, max: 100)
    
    Returns:
        Dictionary containing success status, count, and list of all tickets
    
    Example:
        get_all_tickets(limit=20)
    """
    try:
        # Convert limit to int if it's a string
        limit = int(limit)
        
        if limit < 1 or limit > 100:
            return {
                "success": False,
                "error": "Limit must be between 1 and 100"
            }
        
        tickets = snow_client.get_all_tickets(limit=limit)
        return {
            "success": True,
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_priority_tickets(priority: int = 1, limit: int = 20) -> Dict[str, Any]:
    """
    Get incident tickets filtered by priority level.
    
    Priority levels:
    - 1: Critical
    - 2: High
    - 3: Moderate
    - 4: Low
    - 5: Planning
    
    Args:
        priority: Priority level to filter by (1-5, default: 1)
        limit: Maximum number of tickets to return (default: 20, max: 100)
    
    Returns:
        Dictionary containing success status, priority level, count, and list of tickets
    
    Example:
        get_priority_tickets(priority=1, limit=10)
    """
    try:
        # Convert parameters to int if they're strings
        priority = int(priority)
        limit = int(limit)
        
        if priority < 1 or priority > 5:
            return {
                "success": False,
                "error": "Priority must be between 1 and 5"
            }
        
        if limit < 1 or limit > 100:
            return {
                "success": False,
                "error": "Limit must be between 1 and 100"
            }
        
        tickets = snow_client.get_priority_tickets(priority=priority, limit=limit)
        
        priority_names = {
            1: "Critical",
            2: "High",
            3: "Moderate",
            4: "Low",
            5: "Planning"
        }
        
        return {
            "success": True,
            "priority": priority,
            "priority_name": priority_names.get(priority, "Unknown"),
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_ticket_by_number(ticket_number: str, **kwargs) -> Dict[str, Any]:
    """
    Retrieve a specific ticket by its ticket number.
    
    Args:
        ticket_number: The ticket number (e.g., "INC0010001")
    
    Returns:
        Dictionary containing success status and ticket details
    
    Example:
        get_ticket_by_number("INC0010001")
    """
    try:
        # Ignore any extra parameters passed by the client
        ticket = snow_client.get_ticket_by_number(ticket_number)
        
        if ticket is None:
            return {
                "success": False,
                "error": f"Ticket {ticket_number} not found"
            }
        
        return {
            "success": True,
            "ticket": ticket
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_ticket_statistics() -> Dict[str, Any]:
    """
    Get statistics about tickets in the system.
    
    Provides counts of tickets by priority level.
    
    Returns:
        Dictionary containing ticket statistics by priority
    
    Example:
        get_ticket_statistics()
    """
    try:
        stats = {
            "success": True,
            "statistics": {}
        }
        
        priority_names = {
            1: "Critical",
            2: "High",
            3: "Moderate",
            4: "Low",
            5: "Planning"
        }
        
        total_count = 0
        for priority in range(1, 6):
            tickets = snow_client.get_priority_tickets(priority=priority, limit=100)
            count = len(tickets)
            total_count += count
            stats["statistics"][priority_names[priority]] = {
                "priority_level": priority,
                "count": count
            }
        
        stats["total_tickets"] = total_count
        return stats
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Add resource for server information
@mcp.resource("servicenow://info")
def get_server_info() -> str:
    """
    Get information about the ServiceNow MCP server.
    
    Returns server configuration and available tools.
    """
    return f"""
ServiceNow MCP Server
====================

Instance: {os.getenv('SERVICENOW_INSTANCE', 'Not configured')}
Protocol: SSE (Server-Sent Events)

Available Tools:
- search_tickets: Search for tickets by query
- create_ticket: Create a new incident ticket
- get_all_tickets: Retrieve all tickets
- get_priority_tickets: Get tickets by priority level
- get_ticket_by_number: Get a specific ticket
- get_ticket_statistics: Get ticket statistics

Priority Levels:
1 - Critical
2 - High
3 - Moderate
4 - Low
5 - Planning
"""


# Add prompt for common operations
@mcp.prompt()
def ticket_search_prompt(query: str) -> str:
    """
    Generate a prompt for searching tickets.
    
    Args:
        query: Search query
    """
    return f"Search for ServiceNow tickets related to: {query}"


@mcp.prompt()
def create_incident_prompt(issue: str) -> str:
    """
    Generate a prompt for creating an incident ticket.
    
    Args:
        issue: Description of the issue
    """
    return f"Create a ServiceNow incident ticket for: {issue}"


if __name__ == "__main__":
    # Run the FastMCP server with SSE transport
    mcp.run(transport="sse")

# Made with Bob
