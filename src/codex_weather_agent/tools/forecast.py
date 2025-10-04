"""Weather forecast tool for LangGraph with optimized performance."""

import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Dict, Any, Optional
from functools import lru_cache
from langchain_core.tools import tool

# Global optimized session with retry strategy and connection pooling
_forecast_session: Optional[requests.Session] = None

def get_forecast_session() -> requests.Session:
    """Get a reusable session optimized for forecast requests."""
    global _forecast_session
    if _forecast_session is None:
        _forecast_session = requests.Session()
        retries = Retry(
            total=2,  # Reduced retries for faster response
            backoff_factor=0.3,  # Faster backoff
            status_forcelist=[502, 503, 504, 524],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(
            max_retries=retries,
            pool_connections=10,
            pool_maxsize=20
        )
        _forecast_session.mount("http://", adapter)
        _forecast_session.mount("https://", adapter)
    return _forecast_session

@lru_cache(maxsize=64)
def _cached_forecast_request(url: str) -> Dict[str, Any]:
    """Cache forecast requests to reduce API calls."""
    try:
        session = get_forecast_session()
        response = session.get(url, timeout=(2, 8))  # Optimized timeouts
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_forecast(city: str, api_key: str = None) -> Dict[str, Any]:
    """
    Get 5-day weather forecast with 3-hour intervals using OpenWeatherMap API.
    
    Args:
        city: Name of the city to get forecast data for
        api_key: OpenWeatherMap API key (optional, uses environment variable if not provided)
        
    Returns:
        Dictionary containing forecast data or error information
    """
    if api_key is None:
        api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return {"error": "OpenWeather API key is required. Set OPENWEATHER_API_KEY environment variable or pass api_key parameter."}
    
    # Normalize city name for consistent caching
    city_normalized = city.strip().lower()
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_normalized}&appid={api_key}&units=metric"
    
    return _cached_forecast_request(url)