# week3/server.py

from __future__ import annotations

import logging
import sys

from mcp.server.fastmcp import FastMCP

from week3.tools.geocoding import search_location
from week3.tools.weather import get_weather_forecast

# ---------------------------------------------------------
# Logging
# STDIO MCP server should log to stderr, not stdout
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("weather-mcp-server")

# ---------------------------------------------------------
# MCP App
# ---------------------------------------------------------
mcp = FastMCP("weather-map-server")

# ---------------------------------------------------------
# Tool 1: search_location
# ---------------------------------------------------------
@mcp.tool()
def search_location_tool(
    query: str,
    count: int = 5,
    language: str = "en",
) -> dict:
    """
    Search locations by place name and return candidate results.
    """
    logger.info(
        "Tool called: search_location | query=%r count=%s language=%s",
        query,
        count,
        language,
    )
    return search_location(query=query, count=count, language=language)


# ---------------------------------------------------------
# Tool 2: get_weather_forecast
# ---------------------------------------------------------
@mcp.tool()
def get_weather_forecast_tool(
    latitude: float,
    longitude: float,
    timezone: str = "auto",
    forecast_days: int = 3,
    temperature_unit: str = "celsius",
    wind_speed_unit: str = "kmh",
) -> dict:
    """
    Get current weather and daily forecast by coordinates.
    """
    logger.info(
        (
            "Tool called: get_weather_forecast | "
            "latitude=%s longitude=%s timezone=%s forecast_days=%s "
            "temperature_unit=%s wind_speed_unit=%s"
        ),
        latitude,
        longitude,
        timezone,
        forecast_days,
        temperature_unit,
        wind_speed_unit,
    )
    return get_weather_forecast(
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        forecast_days=forecast_days,
        temperature_unit=temperature_unit,
        wind_speed_unit=wind_speed_unit,
    )


# ---------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------
if __name__ == "__main__":
    logger.info("Starting weather-map-server with STDIO transport...")
    mcp.run(transport="stdio")