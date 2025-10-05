"""
Weather tools package with configurable settings.
"""

from typing import List
from langchain_core.tools import BaseTool

from .current_location import current_location
from .current_weather import get_current_weather  
from .forecast import get_weather_forecast
from .air_pollution import get_air_pollution
from .coordinates import get_location_coordinates
from ..config import WeatherConfig


def get_weather_tools(config: WeatherConfig) -> List[BaseTool]:
    """
    Get configured weather tools.
    
    Args:
        config: Weather configuration
        
    Returns:
        List of configured weather tools
    """
    # Configure tools with the weather config
    tools = [
        current_location,
        get_current_weather,
        get_weather_forecast,
        get_air_pollution, 
        get_location_coordinates
    ]
    
    # Set configuration on tools that need it
    for tool in tools:
        if hasattr(tool, '_weather_config'):
            tool._weather_config = config
    
    return tools


__all__ = [
    "get_weather_tools",
    "current_location",
    "get_current_weather",
    "get_weather_forecast", 
    "get_air_pollution",
    "get_location_coordinates"
]