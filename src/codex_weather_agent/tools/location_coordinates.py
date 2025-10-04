"""Location coordinates tool for LangGraph with optimized performance."""

import os
import requests
from typing import Dict, Any
from functools import lru_cache
from langchain_core.tools import tool

# Reuse session from current_weather for consistency
from .current_weather import get_session

@lru_cache(maxsize=256)
def _cached_geocoding_request(location_key: str, api_key: str) -> Dict[str, Any]:
    """Cache geocoding requests to reduce API calls."""
    try:
        location_name, limit = location_key.rsplit(':', 1)
        session = get_session()
        url = "https://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": location_name,
            "limit": int(limit),
            "appid": api_key
        }
        response = session.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_location_coordinates(location_name: str, limit: int = 1, api_key: str = None) -> Dict[str, Any]:
    """
    Get geographical coordinates for a location using OpenWeatherMap Geocoding API.

    Args:
        location_name: Name of the city or location
        limit: Maximum number of results to return (default: 1)
        api_key: OpenWeatherMap API key (optional, uses environment variable if not provided)

    Returns:
        Dictionary containing location data (lat, lon, and other info) or error information
    """
    if api_key is None:
        api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return {"error": "OpenWeather API key is required. Set OPENWEATHER_API_KEY environment variable or pass api_key parameter."}
    
    # Normalize location name and create cache key
    location_normalized = location_name.strip().lower()
    location_key = f"{location_normalized}:{limit}"
    
    return _cached_geocoding_request(location_key, api_key)