#!/bin/bash

# MCP Server Startup Script

echo "=========================================="
echo "Starting MCP Server for ServiceNow"
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

# Start the server
echo "🚀 Starting MCP Server..."
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python mcp_server.py

# Made with Bob
