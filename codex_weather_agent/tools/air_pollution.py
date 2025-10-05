import requests
from langchain_core.tools import tool
from typing import Dict, Any
import os

# Configuration
DEFAULT_API_KEY = "6181bebdae59b62fa021aa4b0474bc85"
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"


@tool
def get_air_pollution(lat: float, lon: float) -> Dict[str, Any]:
    """
    Get air pollution data for specific coordinates using OpenWeatherMap API with optimized networking.
    
    Args:
        lat (float): Latitude of the location
        lon (float): Longitude of the location
        
    Returns:
        Dict[str, Any]: JSON response containing air pollution data or error information.
                       Uses connection pooling and optimized timeout for better performance.
    """
    # Get API key from config or environment or default
    api_key = getattr(get_air_pollution, '_weather_config', None)
    if api_key and hasattr(api_key, 'openweather_api_key'):
        api_key = api_key.openweather_api_key
    else:
        api_key = os.getenv("OPENWEATHER_API_KEY", DEFAULT_API_KEY)
    
    try:
        # Use context manager for automatic session cleanup
        with requests.Session() as session:
            url = f"{OPENWEATHER_BASE_URL}/air_pollution"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": api_key
            }
            response = session.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
    except requests.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}