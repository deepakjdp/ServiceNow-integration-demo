"""
ServiceNow Client for ticket operations
"""
import pysnow
from typing import List, Dict, Optional, Any
from config import settings


class ServiceNowClient:
    """Client for interacting with ServiceNow API"""
    
    def __init__(self):
        """Initialize ServiceNow client"""
        # Validate configuration
        if not settings.validate_servicenow_config():
            raise ValueError(
                "ServiceNow configuration is incomplete. Please set the following environment variables:\n"
                "- SERVICENOW_INSTANCE\n"
                "- SERVICENOW_USERNAME\n"
                "- SERVICENOW_PASSWORD"
            )
        
        # Clean up instance name - remove .service-now.com if present
        # pysnow will add it automatically
        instance = settings.servicenow_instance
        if instance:
            # Remove common suffixes that pysnow adds automatically
            instance = instance.replace('.service-now.com', '')
            instance = instance.replace('https://', '')
            instance = instance.replace('http://', '')
            instance = instance.strip('/')
        
        self.client = pysnow.Client(
            instance=instance,
            user=settings.servicenow_username,
            password=settings.servicenow_password
        )
        self.incident_resource = self.client.resource(api_path='/table/incident')
    
    def search_tickets(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for tickets based on query
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of ticket dictionaries
        """
        try:
            # Search in short_description and description fields
            qb = (
                pysnow.QueryBuilder()
                .field('short_description').contains(query)
                .OR()
                .field('description').contains(query)
            )
            
            response = self.incident_resource.get(
                query=qb,
                limit=limit
            )
            
            tickets = []
            for record in response.all():
                tickets.append(self._format_ticket(record))
            
            return tickets
        except Exception as e:
            raise Exception(f"Error searching tickets: {str(e)}")
    
    def create_ticket(
        self,
        short_description: str,
        description: str,
        priority: int = 3,
        caller_id: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new incident ticket
        
        Args:
            short_description: Brief description of the issue
            description: Detailed description
            priority: Priority level (1-5, where 1 is highest)
            caller_id: ID of the caller
            category: Ticket category
            
        Returns:
            Created ticket dictionary
        """
        try:
            ticket_data = {
                'short_description': short_description,
                'description': description,
                'priority': priority,
                'state': 1  # New
            }
            
            if caller_id:
                ticket_data['caller_id'] = caller_id
            if category:
                ticket_data['category'] = category
            
            response = self.incident_resource.create(payload=ticket_data)
            return self._format_ticket(response)
        except Exception as e:
            raise Exception(f"Error creating ticket: {str(e)}")
    
    def get_all_tickets(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get all tickets
        
        Args:
            limit: Maximum number of tickets to return
            
        Returns:
            List of ticket dictionaries
        """
        try:
            response = self.incident_resource.get(limit=limit)
            
            tickets = []
            for record in response.all():
                tickets.append(self._format_ticket(record))
            
            return tickets
        except Exception as e:
            raise Exception(f"Error fetching all tickets: {str(e)}")
    
    def get_priority_tickets(self, priority: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Get tickets by priority
        
        Args:
            priority: Priority level (1-5, where 1 is highest)
            limit: Maximum number of tickets to return
            
        Returns:
            List of high priority ticket dictionaries
        """
        try:
            qb = pysnow.QueryBuilder().field('priority').equals(priority)
            
            response = self.incident_resource.get(
                query=qb,
                limit=limit
            )
            
            tickets = []
            for record in response.all():
                tickets.append(self._format_ticket(record))
            
            return tickets
        except Exception as e:
            raise Exception(f"Error fetching priority tickets: {str(e)}")
    
    def get_ticket_by_number(self, ticket_number: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific ticket by its number
        
        Args:
            ticket_number: Ticket number (e.g., INC0010001)
            
        Returns:
            Ticket dictionary or None if not found
        """
        try:
            qb = pysnow.QueryBuilder().field('number').equals(ticket_number)
            response = self.incident_resource.get(query=qb, limit=1)
            
            for record in response.all():
                return self._format_ticket(record)
            
            return None
        except Exception as e:
            raise Exception(f"Error fetching ticket: {str(e)}")
    
    def _format_ticket(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format ticket data for consistent output
        
        Args:
            record: Raw ticket record from ServiceNow
            
        Returns:
            Formatted ticket dictionary
        """
        return {
            'number': record.get('number', ''),
            'sys_id': record.get('sys_id', ''),
            'short_description': record.get('short_description', ''),
            'description': record.get('description', ''),
            'priority': record.get('priority', ''),
            'state': record.get('state', ''),
            'assigned_to': record.get('assigned_to', ''),
            'caller_id': record.get('caller_id', ''),
            'category': record.get('category', ''),
            'created_on': record.get('sys_created_on', ''),
            'updated_on': record.get('sys_updated_on', '')
        }

# Made with Bob
