"""
Configuration module for MCP Server
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # ServiceNow Configuration
    servicenow_instance: Optional[str] = None
    servicenow_username: Optional[str] = None
    servicenow_password: Optional[str] = None
    
    # MCP Server Configuration
    mcp_server_host: str = "0.0.0.0"
    mcp_server_port: int = 10000
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables
    
    def validate_servicenow_config(self) -> bool:
        """Check if ServiceNow configuration is valid"""
        return all([
            self.servicenow_instance,
            self.servicenow_username,
            self.servicenow_password
        ])


# Global settings instance
try:
    settings = Settings()
except Exception as e:
    print(f"Warning: Error loading settings: {e}")
    # Create settings with defaults if loading fails
    settings = Settings(
        servicenow_instance=os.getenv("SERVICENOW_INSTANCE"),
        servicenow_username=os.getenv("SERVICENOW_USERNAME"),
        servicenow_password=os.getenv("SERVICENOW_PASSWORD")
    )

# Made with Bob
