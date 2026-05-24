# FastMCP Server for ServiceNow with SSE Protocol

A Model Context Protocol (MCP) server implementation using FastMCP for ServiceNow operations support activities. This server exposes ServiceNow operations as MCP tools that can be imported and used by AI assistants and other MCP clients.

## What is FastMCP?

FastMCP is a Python framework for building MCP (Model Context Protocol) servers. It allows you to expose functions as tools that can be discovered and called by MCP clients, including AI assistants like Claude.

## Features

### MCP Tools
- **search_tickets**: Search for tickets based on keywords
- **create_ticket**: Create new incident tickets
- **get_all_tickets**: Retrieve all tickets with pagination
- **get_priority_tickets**: Filter tickets by priority level (1-5)
- **get_ticket_by_number**: Get a specific ticket by its number
- **get_ticket_statistics**: Get statistics about tickets by priority

### MCP Resources
- **servicenow://info**: Server information and configuration

### MCP Prompts
- **ticket_search_prompt**: Generate search prompts
- **create_incident_prompt**: Generate incident creation prompts

### Transport
- **SSE (Server-Sent Events)**: Real-time streaming protocol for MCP communication

## Architecture

```
servicenow_sse_demo/
├── fastmcp_server.py       # Main FastMCP server with tool definitions
├── servicenow_client.py    # ServiceNow API client wrapper
├── config.py               # Configuration management
├── mcp_client_example.py   # Example MCP client usage
├── requirements.txt        # Python dependencies (FastMCP)
├── .env.example           # Environment variables template
└── FASTMCP_README.md      # This file
```

## Prerequisites

- Python 3.10 or higher
- ServiceNow instance with API access
- Valid ServiceNow credentials

## Installation

1. **Navigate to the project directory**:
   ```bash
   cd servicenow_sse_demo
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your ServiceNow credentials:
   ```
   SERVICENOW_INSTANCE=your-instance.service-now.com
   SERVICENOW_USERNAME=your-username
   SERVICENOW_PASSWORD=your-password
   ```

## Usage

### Running the FastMCP Server

#### Method 1: Direct Execution
```bash
python fastmcp_server.py
```

The server will start with SSE transport and be ready to accept MCP client connections.

#### Method 2: Using MCP Inspector (for development)
```bash
mcp dev fastmcp_server.py
```

This opens the MCP Inspector UI for testing tools interactively.

### Using with Claude Desktop

Add to your Claude Desktop configuration (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "servicenow": {
      "command": "python",
      "args": ["/path/to/servicenow_sse_demo/fastmcp_server.py"],
      "env": {
        "SERVICENOW_INSTANCE": "your-instance.service-now.com",
        "SERVICENOW_USERNAME": "your-username",
        "SERVICENOW_PASSWORD": "your-password"
      }
    }
  }
}
```

### Using with MCP Client

See `mcp_client_example.py` for a complete example:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["fastmcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Call a tool
            result = await session.call_tool(
                "search_tickets",
                arguments={"query": "network", "limit": 5}
            )
            print(result.content[0].text)

asyncio.run(main())
```

Run the example:
```bash
python mcp_client_example.py
```

## Available Tools

### 1. search_tickets

Search for tickets based on a query string.

**Parameters:**
- `query` (string, required): Search query
- `limit` (integer, optional): Max results (default: 10, max: 100)

**Example:**
```python
result = await session.call_tool(
    "search_tickets",
    arguments={"query": "network issue", "limit": 5}
)
```

### 2. create_ticket

Create a new incident ticket.

**Parameters:**
- `short_description` (string, required): Brief summary
- `description` (string, required): Detailed description
- `priority` (integer, optional): Priority 1-5 (default: 3)
- `caller_id` (string, optional): User ID
- `category` (string, optional): Ticket category

**Example:**
```python
result = await session.call_tool(
    "create_ticket",
    arguments={
        "short_description": "Server down",
        "description": "Production server not responding",
        "priority": 1,
        "category": "hardware"
    }
)
```

### 3. get_all_tickets

Retrieve all tickets.

**Parameters:**
- `limit` (integer, optional): Max results (default: 50, max: 100)

**Example:**
```python
result = await session.call_tool(
    "get_all_tickets",
    arguments={"limit": 20}
)
```

### 4. get_priority_tickets

Get tickets by priority level.

**Parameters:**
- `priority` (integer, optional): Priority 1-5 (default: 1)
- `limit` (integer, optional): Max results (default: 20, max: 100)

**Priority Levels:**
- 1: Critical
- 2: High
- 3: Moderate
- 4: Low
- 5: Planning

**Example:**
```python
result = await session.call_tool(
    "get_priority_tickets",
    arguments={"priority": 1, "limit": 10}
)
```

### 5. get_ticket_by_number

Get a specific ticket by its number.

**Parameters:**
- `ticket_number` (string, required): Ticket number (e.g., "INC0010001")

**Example:**
```python
result = await session.call_tool(
    "get_ticket_by_number",
    arguments={"ticket_number": "INC0010001"}
)
```

### 6. get_ticket_statistics

Get statistics about tickets by priority.

**Parameters:** None

**Example:**
```python
result = await session.call_tool(
    "get_ticket_statistics",
    arguments={}
)
```

## Resources

### servicenow://info

Get server information and configuration.

**Example:**
```python
resource = await session.read_resource("servicenow://info")
print(resource.contents[0].text)
```

## Prompts

### ticket_search_prompt

Generate a search prompt.

**Parameters:**
- `query` (string): Search query

### create_incident_prompt

Generate an incident creation prompt.

**Parameters:**
- `issue` (string): Issue description

## Response Format

All tools return JSON responses with the following structure:

**Success Response:**
```json
{
  "success": true,
  "count": 5,
  "tickets": [...]
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message"
}
```

## Testing

### Using MCP Inspector

```bash
# Install MCP Inspector
pip install mcp-inspector

# Run with inspector
mcp dev fastmcp_server.py
```

This opens a web UI where you can:
- View all available tools
- Test tool calls interactively
- See request/response data
- Debug tool implementations

### Using the Example Client

```bash
python mcp_client_example.py
```

This demonstrates:
- Connecting to the MCP server
- Listing available tools
- Calling various tools
- Reading resources
- Using prompts

## Integration Examples

### With Claude Desktop

Once configured in Claude Desktop, you can use natural language:

```
"Search for all critical priority tickets in ServiceNow"
"Create a ticket for the database connection issue"
"Show me ticket statistics"
```

Claude will automatically use the appropriate MCP tools.

### With Custom Applications

```python
from mcp import ClientSession
import asyncio

async def get_critical_tickets():
    async with create_mcp_session() as session:
        result = await session.call_tool(
            "get_priority_tickets",
            arguments={"priority": 1, "limit": 50}
        )
        return result.content[0].text

tickets = asyncio.run(get_critical_tickets())
```

## Development

### Adding New Tools

1. Define a new function in `fastmcp_server.py`:
```python
@mcp.tool()
def my_new_tool(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    Tool description here.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        Result dictionary
    """
    # Implementation
    return {"success": True, "data": "..."}
```

2. The tool is automatically registered and available to clients.

### Adding Resources

```python
@mcp.resource("servicenow://my-resource")
def my_resource() -> str:
    """Resource description"""
    return "Resource content"
```

### Adding Prompts

```python
@mcp.prompt()
def my_prompt(param: str) -> str:
    """Prompt description"""
    return f"Generated prompt with {param}"
```

## Troubleshooting

### Connection Issues

**Problem:** Cannot connect to ServiceNow
**Solution:** 
- Verify credentials in `.env`
- Check instance URL (no https:// prefix)
- Ensure network connectivity

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'fastmcp'`
**Solution:**
```bash
pip install -r requirements.txt
```

### Tool Not Found

**Problem:** Tool not appearing in client
**Solution:**
- Ensure `@mcp.tool()` decorator is present
- Restart the MCP server
- Check tool function signature

### SSE Transport Issues

**Problem:** SSE connection fails
**Solution:**
- Ensure Python 3.10+
- Check firewall settings
- Verify MCP client supports SSE

## Security Considerations

1. **Credentials**: Never commit `.env` file
2. **Access Control**: Implement authentication for production
3. **Input Validation**: All inputs are validated
4. **Rate Limiting**: Consider adding for production use
5. **Logging**: Monitor tool usage and errors

## Performance Tips

1. **Caching**: Cache frequently accessed tickets
2. **Pagination**: Use appropriate limits
3. **Async Operations**: Tools support async execution
4. **Connection Pooling**: Reuse ServiceNow connections

## Additional Resources

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Specification](https://modelcontextprotocol.io)
- [ServiceNow API Documentation](https://developer.servicenow.com)
- [SSE Protocol](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)

## License

This project is provided as-is for educational and development purposes.

## Support

For issues:
- **FastMCP**: https://github.com/jlowin/fastmcp
- **MCP Protocol**: https://modelcontextprotocol.io
- **ServiceNow API**: ServiceNow documentation

## Contributing

Contributions welcome! Please:
1. Follow PEP 8 style guidelines
2. Add docstrings to all tools
3. Include type hints
4. Test with MCP Inspector
5. Update documentation