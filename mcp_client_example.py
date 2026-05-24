"""
Example MCP Client for ServiceNow Operations
Demonstrates how to connect to and use the FastMCP server
"""
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import json


async def main():
    """Main function to demonstrate MCP client usage"""
    
    # Server parameters for SSE transport
    server_params = StdioServerParameters(
        command="python",
        args=["fastmcp_server.py"],
        env=None
    )
    
    print("=" * 60)
    print("ServiceNow MCP Client Example")
    print("=" * 60)
    print()
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("✅ Connected to MCP server")
            print()
            
            # List available tools
            print("📋 Available Tools:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            print()
            
            # Example 1: Search for tickets
            print("=" * 60)
            print("Example 1: Search Tickets")
            print("=" * 60)
            try:
                result = await session.call_tool(
                    "search_tickets",
                    arguments={
                        "query": "network",
                        "limit": 5
                    }
                )
                print(f"Search Results:")
                print(json.dumps(result.content[0].text, indent=2))
            except Exception as e:
                print(f"Error: {e}")
            print()
            
            # Example 2: Get priority tickets
            print("=" * 60)
            print("Example 2: Get Priority Tickets")
            print("=" * 60)
            try:
                result = await session.call_tool(
                    "get_priority_tickets",
                    arguments={
                        "priority": 1,
                        "limit": 5
                    }
                )
                print(f"Priority 1 (Critical) Tickets:")
                print(json.dumps(result.content[0].text, indent=2))
            except Exception as e:
                print(f"Error: {e}")
            print()
            
            # Example 3: Get all tickets
            print("=" * 60)
            print("Example 3: Get All Tickets")
            print("=" * 60)
            try:
                result = await session.call_tool(
                    "get_all_tickets",
                    arguments={
                        "limit": 10
                    }
                )
                print(f"All Tickets (limited to 10):")
                print(json.dumps(result.content[0].text, indent=2))
            except Exception as e:
                print(f"Error: {e}")
            print()
            
            # Example 4: Get ticket statistics
            print("=" * 60)
            print("Example 4: Get Ticket Statistics")
            print("=" * 60)
            try:
                result = await session.call_tool(
                    "get_ticket_statistics",
                    arguments={}
                )
                print(f"Ticket Statistics:")
                print(json.dumps(result.content[0].text, indent=2))
            except Exception as e:
                print(f"Error: {e}")
            print()
            
            # Example 5: Create a ticket (commented out to avoid creating test tickets)
            print("=" * 60)
            print("Example 5: Create Ticket (Commented Out)")
            print("=" * 60)
            print("To create a ticket, uncomment the following code:")
            print("""
            result = await session.call_tool(
                "create_ticket",
                arguments={
                    "short_description": "Test ticket from MCP",
                    "description": "This is a test ticket created via MCP client",
                    "priority": 3,
                    "category": "inquiry"
                }
            )
            print(json.dumps(result.content[0].text, indent=2))
            """)
            print()
            
            # Example 6: Get specific ticket by number
            print("=" * 60)
            print("Example 6: Get Ticket by Number")
            print("=" * 60)
            print("To get a specific ticket, use:")
            print("""
            result = await session.call_tool(
                "get_ticket_by_number",
                arguments={
                    "ticket_number": "INC0010001"
                }
            )
            print(json.dumps(result.content[0].text, indent=2))
            """)
            print()
            
            # List available resources
            print("=" * 60)
            print("📚 Available Resources:")
            print("=" * 60)
            resources = await session.list_resources()
            for resource in resources.resources:
                print(f"  - {resource.uri}: {resource.name}")
            print()
            
            # Read server info resource
            print("=" * 60)
            print("Server Information:")
            print("=" * 60)
            try:
                resource_content = await session.read_resource("servicenow://info")
                print(resource_content.contents[0].text)
            except Exception as e:
                print(f"Error: {e}")
            print()
            
            # List available prompts
            print("=" * 60)
            print("💬 Available Prompts:")
            print("=" * 60)
            prompts = await session.list_prompts()
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}: {prompt.description}")
            print()
            
            print("=" * 60)
            print("✅ All examples completed!")
            print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
