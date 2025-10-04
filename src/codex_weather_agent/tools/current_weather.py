"""Current weather tool for LangGraph with optimized performance."""

import os
import requests
from typing import Dict, Any, Optional
from functools import lru_cache
from langchain_core.tools import tool

# Global session with connection pooling for better performance
_session: Optional[requests.Session] = None

def get_session() -> requests.Session:
    """Get a reusable session with connection pooling."""
    global _session
    if _session is None:
        _session = requests.Session()
        # Configure connection pooling
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=3
        )
        _session.mount("http://", adapter)
        _session.mount("https://", adapter)
    return _session

@lru_cache(maxsize=128)
def _cached_weather_request(url: str) -> Dict[str, Any]:
    """Cache weather requests to reduce API calls."""
    try:
        session = get_session()
        response = session.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@tool
def get_weather(city: str, api_key: str = None) -> Dict[str, Any]:
    """
    Get current weather data for a given city using OpenWeatherMap API.
    
    Args:
        city: Name of the city to get weather data for
        api_key: OpenWeatherMap API key (optional, uses environment variable if not provided)
        
    Returns:
        Dictionary containing weather data or error information
    """
    if api_key is None:
        api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return {"error": "OpenWeather API key is required. Set OPENWEATHER_API_KEY environment variable or pass api_key parameter."}
    
    # Normalize city name for consistent caching
    city_normalized = city.strip().lower()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_normalized}&appid={api_key}&units=metric"
    
    return _cached_weather_request(url)