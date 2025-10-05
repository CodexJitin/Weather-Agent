import requests
from langchain_core.tools import tool
from typing import Dict, Any, List
import os

# Configuration
DEFAULT_API_KEY = "6181bebdae59b62fa021aa4b0474bc85"
GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"


@tool
def get_location_coordinates(location_name: str, limit: int = 1) -> List[Dict[str, Any]]:
    """
    Get geographical coordinates for a location using OpenWeatherMap Geocoding API with optimized networking.

    Args:
        location_name (str): Name of the city or location
        limit (int, optional): Maximum number of results to return. Defaults to 1.

    Returns:
        List[Dict[str, Any]]: List containing location data (lat, lon, and other info) or error information.
                             Uses connection pooling and optimized timeout for better performance.
    """
    # Get API key from config or environment or default
    api_key = getattr(get_location_coordinates, '_weather_config', None)
    if api_key and hasattr(api_key, 'openweather_api_key'):
        api_key = api_key.openweather_api_key
    else:
        api_key = os.getenv("OPENWEATHER_API_KEY", DEFAULT_API_KEY)
    
    try:
        # Use context manager for automatic session cleanup
        with requests.Session() as session:
            params = {
                "q": location_name,
                "limit": max(1, min(limit, 5)),  # Ensure reasonable limit
                "appid": api_key
            }
            response = session.get(GEOCODING_URL, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Return empty list if no results found
            return data if isinstance(data, list) else []
            
    except requests.RequestException as e:
        return [{"error": f"Network error: {str(e)}"}]
    except Exception as e:
        return [{"error": f"Unexpected error: {str(e)}"}]