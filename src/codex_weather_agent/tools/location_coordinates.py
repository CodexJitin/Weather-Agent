"""Location coordinates tool for LangGraph."""

import os
import requests
from typing import Dict, Any
from langchain_core.tools import tool

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
    
    # Normalize location name
    location_normalized = location_name.strip().lower()
    
    try:
        url = "https://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": location_normalized,
            "limit": limit,
            "appid": api_key
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}