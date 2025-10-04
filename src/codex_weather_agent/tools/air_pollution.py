"""Air pollution tool for LangGraph."""

import os
import requests
from typing import Dict, Any
from langchain_core.tools import tool

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
    
    # Round coordinates for consistency
    lat_rounded = round(lat, 4)
    lon_rounded = round(lon, 4)
    
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat_rounded}&lon={lon_rounded}&appid={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}