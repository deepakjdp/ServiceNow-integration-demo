# ServiceNow MCP Server - Demo Guide

## 🎯 Demo Overview

This demo showcases a Model Context Protocol (MCP) server that integrates with ServiceNow using Server-Sent Events (SSE) for real-time ticket management. The project demonstrates three different implementations:

1. **FastAPI MCP Server** - RESTful API with SSE streaming
2. **FastMCP Server** - MCP protocol implementation for AI assistants
3. **Render Deployment** - Cloud-hosted production deployment

---

## 📋 Demo Preparation Checklist

### Prerequisites
- [ ] Python 3.8+ installed
- [ ] ServiceNow instance access (credentials ready)
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with ServiceNow credentials

### Quick Setup (5 minutes)
```bash
# 1. Clone/navigate to project
cd servicenow_sse_demo

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your ServiceNow credentials

# 5. Verify setup
python -c "from config import Config; print('✓ Configuration loaded')"
```

---

## 🎬 Demo Scenarios

### Demo 1: FastAPI Server with SSE Streaming (10 minutes)

**What to Show:** Real-time ticket streaming using Server-Sent Events

#### Step 1: Start the Server
```bash
python mcp_server.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Step 2: Open the Interactive Web Client
1. Open `example_sse_client.html` in a web browser
2. The interface shows:
   - Connection status indicator
   - Control buttons for different operations
   - Real-time event display area

#### Step 3: Demonstrate SSE Streaming

**A. Stream All Tickets**
1. Click "Stream All Tickets" button
2. Watch tickets appear in real-time
3. Point out:
   - Connection status changes to "Connected"
   - Each ticket streams individually
   - Ticket details (number, description, priority, state)
   - Completion message when done

**B. Stream Priority Tickets**
1. Set Priority to "1" (Critical)
2. Click "Stream Priority Tickets"
3. Show only critical priority tickets streaming

**C. Stream Search Results**
1. Enter search term (e.g., "network")
2. Click "Stream Search Results"
3. Show filtered results streaming in real-time

#### Step 4: Test REST API Endpoints

**Using curl:**
```bash
# Health check
curl http://localhost:8000/health

# Get all tickets
curl http://localhost:8000/tickets/all?limit=5

# Search tickets
curl -X POST http://localhost:8000/tickets/search \
  -H "Content-Type: application/json" \
  -d '{"query": "network", "limit": 5}'

# Create a ticket
curl -X POST http://localhost:8000/tickets/create \
  -H "Content-Type: application/json" \
  -d '{
    "short_description": "Demo ticket",
    "description": "Created during demo",
    "priority": 3
  }'

# Get specific ticket
curl http://localhost:8000/tickets/INC0010001
```

#### Step 5: Show API Documentation
1. Open browser to `http://localhost:8000/docs`
2. Demonstrate Swagger UI:
   - All available endpoints
   - Request/response schemas
   - Try out functionality
3. Show ReDoc: `http://localhost:8000/redoc`

**Key Points to Highlight:**
- ✅ Real-time streaming with SSE
- ✅ RESTful API design
- ✅ Interactive web client
- ✅ Automatic API documentation
- ✅ Error handling and validation

---

### Demo 2: FastMCP Server for AI Integration (10 minutes)

**What to Show:** MCP protocol implementation for AI assistants like Claude

#### Step 1: Start FastMCP Server
```bash
python fastmcp_server.py
```

**Expected Output:**
```
FastMCP Server initialized
Available tools: 6
Transport: SSE
Server ready for MCP connections
```

#### Step 2: Test with MCP Inspector (Development Tool)
```bash
mcp dev fastmcp_server.py
```

This opens a web UI showing:
- All available MCP tools
- Tool schemas and parameters
- Interactive testing interface

#### Step 3: Demonstrate MCP Tools

**Available Tools:**
1. `search_tickets` - Search for tickets
2. `create_ticket` - Create new incidents
3. `get_all_tickets` - Retrieve all tickets
4. `get_priority_tickets` - Filter by priority
5. `get_ticket_by_number` - Get specific ticket
6. `get_ticket_statistics` - Get ticket stats

#### Step 4: Run Example MCP Client
```bash
python mcp_client_example.py
```

**What It Demonstrates:**
- Connecting to MCP server
- Listing available tools
- Calling tools programmatically
- Reading resources
- Using prompts

#### Step 5: Claude Desktop Integration

**Show Configuration:**
```json
{
  "mcpServers": {
    "servicenow": {
      "command": "python",
      "args": ["/path/to/fastmcp_server.py"],
      "env": {
        "SERVICENOW_INSTANCE": "your-instance.service-now.com",
        "SERVICENOW_USERNAME": "your-username",
        "SERVICENOW_PASSWORD": "your-password"
      }
    }
  }
}
```

**Demo Natural Language Commands:**
- "Search for all critical priority tickets"
- "Create a ticket for database connection issue"
- "Show me ticket statistics"
- "Get details for ticket INC0010001"

**Key Points to Highlight:**
- ✅ MCP protocol compliance
- ✅ AI assistant integration
- ✅ Natural language interface
- ✅ Tool discovery and schema
- ✅ Async operation support

---

### Demo 3: Cloud Deployment on Render (5 minutes)

**What to Show:** Production-ready cloud deployment

#### Step 1: Show Render Dashboard
1. Navigate to https://dashboard.render.com
2. Show deployed service: `servicenow-mcp-server`
3. Point out:
   - Service status (Live)
   - Deployment history
   - Environment variables (configured securely)
   - Logs and monitoring

#### Step 2: Access Live Server
```bash
# Test live endpoint
curl https://servicenow-mcp-server.onrender.com/health

# Test SSE endpoint
curl -N https://servicenow-mcp-server.onrender.com/sse
```

#### Step 3: Show Configuration
1. Environment variables setup
2. `render.yaml` configuration
3. Automatic deployments from Git

**Key Points to Highlight:**
- ✅ Zero-downtime deployments
- ✅ Automatic HTTPS
- ✅ Environment variable management
- ✅ Logging and monitoring
- ✅ Scalability

---

## 🎨 Demo Flow Suggestions

### Quick Demo (5 minutes)
1. Start FastAPI server
2. Open web client
3. Stream all tickets
4. Show API docs

### Standard Demo (15 minutes)
1. FastAPI server + web client (7 min)
2. FastMCP server + MCP Inspector (5 min)
3. Show Render deployment (3 min)

### Full Demo (30 minutes)
1. FastAPI server with all endpoints (10 min)
2. FastMCP server with Claude integration (10 min)
3. Render deployment and monitoring (5 min)
4. Q&A and architecture discussion (5 min)

---

## 💡 Demo Tips

### Before the Demo
1. **Test everything** - Run through the entire demo beforehand
2. **Prepare data** - Ensure ServiceNow has sample tickets
3. **Check credentials** - Verify all credentials work
4. **Browser tabs** - Pre-open relevant URLs
5. **Terminal windows** - Have multiple terminals ready

### During the Demo
1. **Start with the problem** - Explain why this solution exists
2. **Show, don't tell** - Let the audience see it working
3. **Highlight key features** - Point out unique capabilities
4. **Handle errors gracefully** - Have backup plans
5. **Engage the audience** - Ask questions, get feedback

### Common Issues and Solutions

**Issue: Server won't start**
- Check if port 8000 is already in use
- Verify virtual environment is activated
- Check `.env` file exists and is configured

**Issue: No tickets showing**
- Verify ServiceNow credentials
- Check network connectivity
- Look at server logs for errors

**Issue: SSE not streaming**
- Use `curl -N` flag for no buffering
- Check browser console for errors
- Verify CORS settings if needed

---

## 📊 Key Metrics to Highlight

### Performance
- Real-time streaming with minimal latency
- Handles 100+ tickets efficiently
- Async operations for scalability

### Features
- 6 MCP tools available
- 7 REST API endpoints
- 3 SSE streaming endpoints
- Full API documentation

### Integration
- Works with Claude Desktop
- Compatible with any MCP client
- RESTful API for any HTTP client
- WebSocket-like SSE for real-time updates

---

## 🎯 Talking Points

### Architecture
- **Modular design** - Separate concerns (client, server, config)
- **Multiple interfaces** - REST, SSE, MCP protocol
- **Cloud-ready** - Deployed on Render with zero config
- **Extensible** - Easy to add new tools and endpoints

### Technology Stack
- **FastAPI** - Modern, fast Python web framework
- **FastMCP** - MCP protocol implementation
- **SSE** - Real-time streaming without WebSockets
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server for production

### Use Cases
- **IT Operations** - Ticket management and monitoring
- **AI Assistants** - Natural language ticket operations
- **Automation** - Programmatic ticket handling
- **Dashboards** - Real-time ticket streaming
- **Integration** - Connect ServiceNow to other systems

---

## 📝 Demo Script Template

### Introduction (2 minutes)
"Today I'll demonstrate a ServiceNow integration using the Model Context Protocol with Server-Sent Events. This solution enables real-time ticket management through multiple interfaces: a REST API, SSE streaming, and MCP tools for AI assistants."

### Problem Statement (1 minute)
"Organizations need efficient ways to interact with ServiceNow tickets. Traditional polling is inefficient, and integrating with AI assistants requires standardized protocols."

### Solution Overview (2 minutes)
"Our solution provides three key capabilities:
1. RESTful API for standard operations
2. SSE streaming for real-time updates
3. MCP protocol for AI assistant integration"

### Live Demo (10-20 minutes)
[Follow one of the demo scenarios above]

### Architecture Discussion (3 minutes)
"The architecture consists of:
- ServiceNow client wrapper
- FastAPI server with SSE support
- FastMCP server for MCP protocol
- Cloud deployment on Render"

### Conclusion (2 minutes)
"This solution demonstrates modern integration patterns: real-time streaming, AI-ready protocols, and cloud-native deployment. It's production-ready and easily extensible."

---

## 🔗 Quick Reference Links

### Documentation
- Main README: `README.md`
- FastMCP Guide: `FASTMCP_README.md`
- Render Setup: `RENDER_SETUP_GUIDE.md`

### Live Endpoints (Local)
- Server: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Web Client: `example_sse_client.html`

### Live Endpoints (Production)
- Server: https://servicenow-mcp-server.onrender.com
- SSE: https://servicenow-mcp-server.onrender.com/sse

### Code Files
- FastAPI Server: `mcp_server.py`
- FastMCP Server: `fastmcp_server.py`
- ServiceNow Client: `servicenow_client.py`
- Web Client: `example_sse_client.html`
- MCP Client Example: `mcp_client_example.py`

---

## 🎓 Additional Resources

### For Developers
- FastAPI: https://fastapi.tiangolo.com/
- FastMCP: https://github.com/jlowin/fastmcp
- MCP Spec: https://modelcontextprotocol.io
- SSE: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events

### For Operations
- ServiceNow API: https://developer.servicenow.com
- Render Docs: https://render.com/docs
- Python Best Practices: https://peps.python.org/pep-0008/

---

## ✅ Post-Demo Checklist

- [ ] Stop all running servers
- [ ] Deactivate virtual environment
- [ ] Save any demo data/logs
- [ ] Note any issues encountered
- [ ] Gather feedback from audience
- [ ] Update documentation based on questions
- [ ] Share demo recording (if recorded)

---

**Good luck with your demo! 🚀**

*This guide was created to help you deliver an effective demonstration of the ServiceNow MCP Server project.*