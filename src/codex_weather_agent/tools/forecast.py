"""Weather forecast tool for LangGraph."""

import os
import requests
from typing import Dict, Any
from langchain_core.tools import tool

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
    
    # Normalize city name
    city_normalized = city.strip().lower()
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city_normalized}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}