# main.py
from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from infra.database import init_db
from server.tools import register_tools
from core.auth import StaticTokenVerifier
from core.config import settings

# 1. Security verification
auth_config = AuthSettings(
    issuer_url="http://localhost:8000",
    resource_server_url="http://localhost:8000",
    required_scopes=["read", "write"]
)

# 2. Initialize FastMCP with network configuration for Docker
mcp = FastMCP(
    name=settings.APP_NAME, 
    host=settings.HOST, 
    port=settings.PORT,
    auth=auth_config,
    token_verifier=StaticTokenVerifier(),
    log_level=settings.FASTMCP_LOG_LEVEL,
    debug=settings.FASTMCP_DEBUG
    )

# 3. Initialize the database (Create tables)
init_db()

# 4. Register tools from the tools module
register_tools(mcp)

# 5. Entry point
if __name__ == "__main__":
    # Run the server (using SSE transport as required)
    mcp.run(transport="sse")