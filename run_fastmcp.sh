#!/bin/bash

# FastMCP Server Startup Script

echo "=========================================="
echo "Starting FastMCP Server for ServiceNow"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please copy .env.example to .env and configure your ServiceNow credentials."
    echo ""
    echo "Run: cp .env.example .env"
    echo "Then edit .env with your ServiceNow details."
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Start the FastMCP server
echo "🚀 Starting FastMCP Server with SSE transport..."
echo ""
echo "The server is now running and ready to accept MCP client connections."
echo "Use this server with:"
echo "  - Claude Desktop (add to claude_desktop_config.json)"
echo "  - MCP Inspector (run: mcp dev fastmcp_server.py)"
echo "  - Custom MCP clients (see mcp_client_example.py)"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python fastmcp_server.py

# Made with Bob
