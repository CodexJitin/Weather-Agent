"""Air pollution tool for LangGraph with optimized performance."""

import os
import requests
from typing import Dict, Any, Optional, Tuple
from functools import lru_cache
from langchain_core.tools import tool

# Reuse session from current_weather for consistency
from .current_weather import get_session

@lru_cache(maxsize=128)
def _cached_pollution_request(lat_lon_key: str, api_key: str) -> Dict[str, Any]:
    """Cache pollution requests to reduce API calls."""
    try:
        lat, lon = lat_lon_key.split(',')
        session = get_session()
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        response = session.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_air_pollution(lat: float, lon: float, api_key: str = None) -> Dict[str, Any]:
    """
    Get air pollution data for specific coordinates using OpenWeatherMap API.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
        api_key: OpenWeatherMap API key (optional, uses environment variable if not provided)
        
    Returns:
        Dictionary containing air pollution data or error information
    """
    if api_key is None:
        api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return {"error": "OpenWeather API key is required. Set OPENWEATHER_API_KEY environment variable or pass api_key parameter."}
    
    # Round coordinates for better caching (precision to 4 decimal places is sufficient)
    lat_rounded = round(lat, 4)
    lon_rounded = round(lon, 4)
    lat_lon_key = f"{lat_rounded},{lon_rounded}"
    
    return _cached_pollution_request(lat_lon_key, api_key)