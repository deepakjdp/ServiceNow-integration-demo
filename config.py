"""
Configuration module for MCP Server
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # ServiceNow Configuration
    servicenow_instance: str
    servicenow_username: str
    servicenow_password: str
    
    # MCP Server Configuration
    mcp_server_host: str = "0.0.0.0"
    mcp_server_port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Made with Bob
