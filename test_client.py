"""
Test client for MCP Server
Demonstrates how to interact with the server endpoints
"""
import requests
import json
from typing import Dict, Any


class MCPTestClient:
    """Test client for MCP Server"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize test client"""
        self.base_url = base_url
    
    def test_health(self) -> Dict[str, Any]:
        """Test health check endpoint"""
        print("\n=== Testing Health Check ===")
        response = requests.get(f"{self.base_url}/health")
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        return result
    
    def test_root(self) -> Dict[str, Any]:
        """Test root endpoint"""
        print("\n=== Testing Root Endpoint ===")
        response = requests.get(f"{self.base_url}/")
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(result, indent=2)}")
        return result
    
    def test_search_tickets(self, query: str, limit: int = 5) -> Dict[str, Any]:
        """Test ticket search"""
        print(f"\n=== Testing Ticket Search: '{query}' ===")
        response = requests.post(
            f"{self.base_url}/tickets/search",
            json={"query": query, "limit": limit}
        )
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Found {result.get('count', 0)} tickets")
        if result.get('tickets'):
            print(f"First ticket: {json.dumps(result['tickets'][0], indent=2)}")
        return result
    
    def test_create_ticket(
        self,
        short_description: str,
        description: str,
        priority: int = 3
    ) -> Dict[str, Any]:
        """Test ticket creation"""
        print(f"\n=== Testing Ticket Creation ===")
        response = requests.post(
            f"{self.base_url}/tickets/create",
            json={
                "short_description": short_description,
                "description": description,
                "priority": priority
            }
        )
        result = response.json()
        print(f"Status: {response.status_code}")
        if result.get('success'):
            print(f"Created ticket: {result['ticket'].get('number')}")
            print(f"Ticket details: {json.dumps(result['ticket'], indent=2)}")
        return result
    
    def test_get_all_tickets(self, limit: int = 5) -> Dict[str, Any]:
        """Test getting all tickets"""
        print(f"\n=== Testing Get All Tickets (limit={limit}) ===")
        response = requests.get(f"{self.base_url}/tickets/all?limit={limit}")
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Found {result.get('count', 0)} tickets")
        return result
    
    def test_priority_tickets(self, priority: int = 1, limit: int = 5) -> Dict[str, Any]:
        """Test getting priority tickets"""
        print(f"\n=== Testing Priority {priority} Tickets ===")
        response = requests.post(
            f"{self.base_url}/tickets/priority",
            json={"priority": priority, "limit": limit}
        )
        result = response.json()
        print(f"Status: {response.status_code}")
        print(f"Found {result.get('count', 0)} priority {priority} tickets")
        return result
    
    def test_sse_stream(self, endpoint: str, params: Dict[str, Any] = None):
        """Test SSE streaming endpoint"""
        print(f"\n=== Testing SSE Stream: {endpoint} ===")
        url = f"{self.base_url}{endpoint}"
        if params:
            url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
        print(f"Connecting to: {url}")
        
        try:
            response = requests.get(url, stream=True, timeout=30)
            print(f"Status: {response.status_code}")
            
            event_count = 0
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    print(line)
                    event_count += 1
                    
                    # Limit output for testing
                    if event_count > 20:
                        print("... (truncated for brevity)")
                        break
            
            print(f"Received {event_count} events")
        except Exception as e:
            print(f"Error: {str(e)}")


def main():
    """Run all tests"""
    client = MCPTestClient()
    
    print("=" * 60)
    print("MCP Server Test Suite")
    print("=" * 60)
    
    # Test basic endpoints
    client.test_health()
    client.test_root()
    
    # Test ticket operations
    # Note: These will fail if ServiceNow is not configured
    # Uncomment when ServiceNow credentials are set up
    
    # client.test_get_all_tickets(limit=3)
    # client.test_search_tickets("network", limit=3)
    # client.test_priority_tickets(priority=1, limit=3)
    # client.test_create_ticket(
    #     short_description="Test ticket from MCP",
    #     description="This is a test ticket created via MCP server",
    #     priority=3
    # )
    
    # Test SSE streaming
    # client.test_sse_stream("/tickets/stream/all", {"limit": 5})
    # client.test_sse_stream("/tickets/stream/priority/1", {"limit": 3})
    # client.test_sse_stream("/tickets/stream/search", {"query": "network", "limit": 3})
    
    print("\n" + "=" * 60)
    print("Test Suite Complete")
    print("=" * 60)
    print("\nNote: ServiceNow-dependent tests are commented out.")
    print("Uncomment them in test_client.py after configuring .env file.")


if __name__ == "__main__":
    main()

# Made with Bob
