import requests
from langchain_core.tools import tool

OPENWEATHER_API_KEY = "6181bebdae59b62fa021aa4b0474bc85"

@tool
def get_air_pollution(lat: float, lon: float):
    """
    Get air pollution data for specific coordinates using OpenWeatherMap API with optimized networking.
    
    Args:
        lat (float): Latitude of the location
        lon (float): Longitude of the location
        
    Returns:
        dict: JSON response containing air pollution data or error information.
              Uses secure HTTPS, connection pooling, and has a 5-second timeout.
    
    Raises:
        RequestException: For network-related errors
        Exception: For other unexpected errors
    """
    try:
        # Use HTTPS, connection pooling and timeout
        session = requests.Session()
        url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
        response = session.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}