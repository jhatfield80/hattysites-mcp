"""
Hatty.ai MCP Server - main.py
Entry point for the MCP server at mcp.hattysites.com
Exposes Google Ads, Meta Ads, GA4, and Search Console data
as MCP tools for Claude agents.
"""

import asyncio
import logging
import os
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from connectors.google_ads import GoogleAdsConnector
from connectors.meta_ads import MetaAdsConnector
from connectors.ga4 import GA4Connector
from connectors.search_console import SearchConsoleConnector
from tools.google_tools import register_google_tools
from tools.meta_tools import register_meta_tools
from tools.cross_platform_tools import register_cross_platform_tools, execute_cross_platform
from auth import AuthManager

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s [Hatty.ai MCP] %(levelname)s %(message)s"
)
logger = logging.getLogger("hatty-mcp")

# Initialize MCP server
app = Server("hatty-ai-mcp")
auth = AuthManager()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Return all available Hatty.ai MCP tools."""
    tools = []
    tools.extend(register_google_tools())
    tools.extend(register_meta_tools())
    tools.extend(register_cross_platform_tools())
    logger.info(f"Registered {len(tools)} MCP tools")
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Route tool calls to the appropriate connector."""
    logger.info(f"Tool called: {name} | Client: {arguments.get('client_id', 'unknown')}")

    client_id = arguments.get("client_id", "default")

    try:
        if name.startswith("google_"):
            connector = GoogleAdsConnector(
                credentials=auth.get_google_credentials(client_id),
                customer_id=arguments.get("customer_id", "")
            )
            result = await connector.execute(name, arguments)

        elif name.startswith("meta_"):
            connector = MetaAdsConnector(
                access_token=auth.get_meta_token(client_id),
                ad_account_id=arguments.get("ad_account_id", "")
            )
            result = await connector.execute(name, arguments)

        elif name.startswith("ga4_"):
            connector = GA4Connector(
                credentials=auth.get_google_credentials(client_id),
                property_id=arguments.get("property_id", "")
            )
            result = await connector.execute(name, arguments)

        elif name.startswith("cross_"):
            g_connector = GoogleAdsConnector(
                credentials=auth.get_google_credentials(client_id),
                customer_id=arguments.get("customer_id", "")
            )
            m_connector = MetaAdsConnector(
                access_token=auth.get_meta_token(client_id),
                ad_account_id=arguments.get("ad_account_id", "")
            )
            result = await execute_cross_platform(name, arguments, g_connector, m_connector)

        else:
            result = {"error": f"Unknown tool: {name}"}

        return [TextContent(type="text", text=str(result))]

    except FileNotFoundError as e:
        logger.error(f"Credentials not found for client '{client_id}': {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}. Run setup_client.py to onboard this client.")]
    except Exception as e:
        logger.error(f"Tool error: {name} | {e}", exc_info=True)
        return [TextContent(type="text", text=f"Error executing {name}: {str(e)}")]


@app.list_resources()
async def list_resources():
    """List available resources (health check endpoint)."""
    return []


async def main():
    logger.info("Hatty.ai MCP Server starting on mcp.hattysites.com...")
    logger.info("Connecting to MCP transport...")
    async with stdio_server() as (read_stream, write_stream):
        logger.info("MCP Server ready. Waiting for connections.")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
