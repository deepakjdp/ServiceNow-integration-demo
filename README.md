# MCP Server for ServiceNow with SSE Protocol

A Model Context Protocol (MCP) server implementation in Python with Server-Sent Events (SSE) protocol for ServiceNow operations support activities.

## Features

- **Ticket Search**: Search for tickets based on keywords
- **Ticket Creation**: Create new incident tickets
- **Display All Tickets**: Retrieve and display all tickets
- **Priority Tickets**: Filter and display tickets by priority level
- **SSE Streaming**: Real-time ticket streaming using Server-Sent Events
- **RESTful API**: Standard HTTP endpoints for all operations

## Architecture

```
servicenow_sse_demo/
├── mcp_server.py           # Main MCP server with FastAPI and SSE
├── servicenow_client.py    # ServiceNow API client wrapper
├── config.py               # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Prerequisites

- Python 3.8 or higher
- ServiceNow instance with API access
- Valid ServiceNow credentials

## Installation

1. **Clone or navigate to the project directory**:
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
   MCP_SERVER_HOST=0.0.0.0
   MCP_SERVER_PORT=8000
   ```

## Usage

### Starting the Server

Run the MCP server:
```bash
python mcp_server.py
```

The server will start on `http://localhost:8000` (or your configured host/port).

### API Endpoints

#### 1. Root Endpoint
```bash
GET /
```
Returns server information and available endpoints.

#### 2. Health Check
```bash
GET /health
```
Returns server health status.

#### 3. Search Tickets
```bash
POST /tickets/search
Content-Type: application/json

{
  "query": "network issue",
  "limit": 10
}
```

#### 4. Create Ticket
```bash
POST /tickets/create
Content-Type: application/json

{
  "short_description": "Server down",
  "description": "Production server is not responding",
  "priority": 1,
  "caller_id": "user123",
  "category": "hardware"
}
```

#### 5. Get All Tickets
```bash
GET /tickets/all?limit=50
```

#### 6. Get Priority Tickets
```bash
POST /tickets/priority
Content-Type: application/json

{
  "priority": 1,
  "limit": 20
}
```

#### 7. Get Specific Ticket
```bash
GET /tickets/{ticket_number}
```
Example: `GET /tickets/INC0010001`

### SSE Streaming Endpoints

#### Stream All Tickets
```bash
GET /tickets/stream/all?limit=50
```

#### Stream Priority Tickets
```bash
GET /tickets/stream/priority/{priority}?limit=20
```
Example: `GET /tickets/stream/priority/1?limit=20`

#### Stream Search Results
```bash
GET /tickets/stream/search?query=network&limit=10
```

### SSE Event Types

The SSE endpoints emit the following event types:

- **connected**: Initial connection established
- **count**: Total number of tickets to be streamed
- **ticket**: Individual ticket data
- **complete**: Streaming completed
- **error**: Error occurred during streaming

### Example: Consuming SSE Stream

**Using curl**:
```bash
curl -N http://localhost:8000/tickets/stream/all?limit=10
```

**Using JavaScript**:
```javascript
const eventSource = new EventSource('http://localhost:8000/tickets/stream/all?limit=10');

eventSource.addEventListener('connected', (e) => {
  console.log('Connected:', JSON.parse(e.data));
});

eventSource.addEventListener('ticket', (e) => {
  const data = JSON.parse(e.data);
  console.log(`Ticket ${data.index}:`, data.ticket);
});

eventSource.addEventListener('complete', (e) => {
  console.log('Complete:', JSON.parse(e.data));
  eventSource.close();
});

eventSource.addEventListener('error', (e) => {
  console.error('Error:', JSON.parse(e.data));
  eventSource.close();
});
```

**Using Python**:
```python
import requests
import json

response = requests.get(
    'http://localhost:8000/tickets/stream/all?limit=10',
    stream=True
)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = json.loads(line[6:])
            print(data)
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVICENOW_INSTANCE` | ServiceNow instance URL | Required |
| `SERVICENOW_USERNAME` | ServiceNow username | Required |
| `SERVICENOW_PASSWORD` | ServiceNow password | Required |
| `MCP_SERVER_HOST` | Server host address | 0.0.0.0 |
| `MCP_SERVER_PORT` | Server port number | 8000 |

### Priority Levels

ServiceNow uses the following priority levels:
- **1**: Critical
- **2**: High
- **3**: Moderate
- **4**: Low
- **5**: Planning

## Error Handling

The server returns appropriate HTTP status codes:
- **200**: Success
- **400**: Bad Request (invalid parameters)
- **404**: Not Found (ticket doesn't exist)
- **500**: Internal Server Error (ServiceNow API error)

Error responses include a detail message:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Development

### Running in Development Mode

```bash
uvicorn mcp_server:app --reload --host 0.0.0.0 --port 8000
```

### Testing Endpoints

Use tools like:
- **curl**: Command-line HTTP client
- **Postman**: API testing platform
- **HTTPie**: User-friendly HTTP client
- **Browser**: For GET requests and SSE streams

## Security Considerations

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use HTTPS in production** - Encrypt data in transit
3. **Implement authentication** - Add API key or OAuth for production use
4. **Rate limiting** - Consider adding rate limiting for production
5. **Input validation** - All inputs are validated using Pydantic models

## Troubleshooting

### Connection Issues
- Verify ServiceNow credentials in `.env`
- Check ServiceNow instance URL (no https:// prefix)
- Ensure network connectivity to ServiceNow instance

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment if using one

### SSE Stream Not Working
- Use `-N` flag with curl to disable buffering
- Ensure client supports SSE (EventSource API)
- Check firewall/proxy settings

## License

This project is provided as-is for educational and development purposes.

## Support

For issues related to:
- **ServiceNow API**: Consult ServiceNow documentation
- **FastAPI**: Visit https://fastapi.tiangolo.com/
- **SSE**: Check https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events

## Contributing

Contributions are welcome! Please ensure:
1. Code follows PEP 8 style guidelines
2. All endpoints are documented
3. Error handling is implemented
4. Tests are included (if applicable)