"""
FastMCP Server for ServiceNow Operations with SSE Protocol - Render Deployment Version
Model Context Protocol server that exposes ServiceNow operations as tools
"""
from fastmcp import FastMCP
from typing import Optional, List, Dict, Any
import os
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

from servicenow_client import ServiceNowClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("ServiceNow Operations")

# Initialize ServiceNow client with error handling
try:
    snow_client = ServiceNowClient()
    logger.info("✓ ServiceNow client initialized successfully")
    logger.info(f"Connected to instance: {os.getenv('SERVICENOW_INSTANCE', 'Unknown')}")
except ValueError as e:
    logger.error(f"✗ Configuration Error: {e}")
    logger.error("\nPlease configure the following environment variables in Render:")
    logger.error("1. Go to your Render dashboard")
    logger.error("2. Select your web service")
    logger.error("3. Go to Environment tab")
    logger.error("4. Add the following environment variables:")
    logger.error("   - SERVICENOW_INSTANCE (e.g., dev12345)")
    logger.error("   - SERVICENOW_USERNAME")
    logger.error("   - SERVICENOW_PASSWORD")
    sys.exit(1)
except Exception as e:
    logger.error(f"✗ Unexpected error initializing ServiceNow client: {e}")
    sys.exit(1)


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
    logger.info(f"🔍 search_tickets called - query: '{query}', limit: {limit}")
    try:
        # Convert limit to int if it's a string
        limit = int(limit)
        
        if limit < 1 or limit > 100:
            logger.warning(f"Invalid limit value: {limit}")
            return {
                "success": False,
                "error": "Limit must be between 1 and 100"
            }
        
        tickets = snow_client.search_tickets(query=query, limit=limit)
        logger.info(f"✓ Found {len(tickets)} tickets matching query '{query}'")
        return {
            "success": True,
            "count": len(tickets),
            "query": query,
            "tickets": tickets
        }
    except Exception as e:
        logger.error(f"✗ Error searching tickets: {str(e)}")
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
    logger.info(f"📝 create_ticket called - short_description: '{short_description}', priority: {priority}, category: {category}")
    try:
        if priority < 1 or priority > 5:
            logger.warning(f"Invalid priority value: {priority}")
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
        ticket_number = ticket.get('number', 'Unknown')
        logger.info(f"✓ Ticket {ticket_number} created successfully")
        return {
            "success": True,
            "message": f"Ticket {ticket_number} created successfully",
            "ticket": ticket
        }
    except Exception as e:
        logger.error(f"✗ Error creating ticket: {str(e)}")
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
    logger.info(f"📋 get_all_tickets called - limit: {limit}")
    try:
        # Convert limit to int if it's a string
        limit = int(limit)
        
        if limit < 1 or limit > 100:
            logger.warning(f"Invalid limit value: {limit}")
            return {
                "success": False,
                "error": "Limit must be between 1 and 100"
            }
        
        tickets = snow_client.get_all_tickets(limit=limit)
        logger.info(f"✓ Retrieved {len(tickets)} tickets")
        return {
            "success": True,
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        logger.error(f"✗ Error retrieving tickets: {str(e)}")
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
    priority_names = {
        1: "Critical",
        2: "High",
        3: "Moderate",
        4: "Low",
        5: "Planning"
    }
    logger.info(f"🎯 get_priority_tickets called - priority: {priority} ({priority_names.get(priority, 'Unknown')}), limit: {limit}")
    try:
        # Convert parameters to int if they're strings
        priority = int(priority)
        limit = int(limit)
        
        if priority < 1 or priority > 5:
            logger.warning(f"Invalid priority value: {priority}")
            return {
                "success": False,
                "error": "Priority must be between 1 and 5"
            }
        
        if limit < 1 or limit > 100:
            logger.warning(f"Invalid limit value: {limit}")
            return {
                "success": False,
                "error": "Limit must be between 1 and 100"
            }
        
        tickets = snow_client.get_priority_tickets(priority=priority, limit=limit)
        logger.info(f"✓ Found {len(tickets)} tickets with priority {priority} ({priority_names.get(priority)})")
        
        return {
            "success": True,
            "priority": priority,
            "priority_name": priority_names.get(priority, "Unknown"),
            "count": len(tickets),
            "tickets": tickets
        }
    except Exception as e:
        logger.error(f"✗ Error retrieving priority tickets: {str(e)}")
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
    logger.info(f"🎫 get_ticket_by_number called - ticket_number: {ticket_number}")
    try:
        # Ignore any extra parameters passed by the client
        ticket = snow_client.get_ticket_by_number(ticket_number)
        
        if ticket is None:
            logger.warning(f"Ticket {ticket_number} not found")
            return {
                "success": False,
                "error": f"Ticket {ticket_number} not found"
            }
        
        logger.info(f"✓ Retrieved ticket {ticket_number}")
        return {
            "success": True,
            "ticket": ticket
        }
    except Exception as e:
        logger.error(f"✗ Error retrieving ticket {ticket_number}: {str(e)}")
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
    logger.info("📊 get_ticket_statistics called")
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
            logger.info(f"  - {priority_names[priority]}: {count} tickets")
        
        stats["total_tickets"] = total_count
        logger.info(f"✓ Total tickets: {total_count}")
        return stats
        
    except Exception as e:
        logger.error(f"✗ Error retrieving ticket statistics: {str(e)}")
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
ServiceNow MCP Server (Render Deployment)
==========================================

Instance: {os.getenv('SERVICENOW_INSTANCE', 'Not configured')}
Protocol: SSE (Server-Sent Events)
Environment: Render Cloud

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
    # Get port from environment variable (Render provides this)
    port = int(os.getenv("PORT", 10000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting FastMCP server")
    print(f"📡 Transport: SSE (Server-Sent Events)")
    print(f"🔌 Port: {port} (from environment)")
    print(f"🌐 Host: {host}")
    print(f"🔗 ServiceNow Instance: {os.getenv('SERVICENOW_INSTANCE', 'Not configured')}")
    print("-" * 50)
    
    # FastMCP's run() method doesn't accept host/port parameters
    # It reads from environment variables internally when using SSE transport
    # Make sure PORT and HOST are set in environment
    os.environ["PORT"] = str(port)
    os.environ["HOST"] = host
    
    # Run the FastMCP server with SSE transport
    # The SSE transport will use uvicorn which reads PORT and HOST from environment
    mcp.run(transport="sse")

# Made with Bob
