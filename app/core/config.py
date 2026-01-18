# core/config.py
import os
from dataclasses import dataclass

@dataclass
class Settings:
    """
    Centralized configuration settings for the application.
    """
    APP_NAME: str = os.getenv("APP_NAME", "Real Estate MCP Server")
    API_TOKEN: str = os.getenv("APP_API_TOKEN", "secret_token_2026")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/real_estate.db")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    FASTMCP_DEBUG: bool = os.getenv("FASTMCP_DEBUG", "False").lower() == "true"
    FASTMCP_LOG_LEVEL: str = os.getenv("FASTMCP_LOG_LEVEL", "INFO")

settings = Settings()