import requests
from langchain_core.tools import tool

OPENWEATHER_API_KEY = "6181bebdae59b62fa021aa4b0474bc85"

@tool
def get_location_coordinates(location_name: str, limit: int = 1):
    """
    Get geographical coordinates for a location using OpenWeatherMap Geocoding API with optimized networking.

    Args:
        location_name (str): Name of the city or location
        limit (int, optional): Maximum number of results to return. Defaults to 1.

    Returns:
        dict: JSON response containing location data (lat, lon, and other info) or error information.
             Uses secure HTTPS, connection pooling, and has a 5-second timeout.

    Raises:
        RequestException: For network-related errors
        Exception: For other unexpected errors
    """
    try:
        # Use HTTPS, connection pooling, timeout, and request params
        session = requests.Session()
        url = "https://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": location_name,
            "limit": limit,
            "appid": OPENWEATHER_API_KEY
        }
        response = session.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}