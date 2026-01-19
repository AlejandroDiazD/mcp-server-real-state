# core/auth.py
from mcp.server.auth.provider import TokenVerifier, AccessToken
from core.config import settings
import logging

class StaticTokenVerifier(TokenVerifier):
    """
    Official way to verify tokens in FastMCP.
    It checks if the Bearer token matches our settings.
    """
    async def verify_token(self, token: str) -> AccessToken | None:
        clean_token = token.replace("Bearer ", "").replace("bearer ", "").strip()
        if clean_token == settings.API_TOKEN:
            return AccessToken(
                token=clean_token,
                client_id="admin-user",
                scopes=["read", "write"],
                expires_at=None 
            )
        return None