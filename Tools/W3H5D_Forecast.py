import requests
from langchain_core.tools import tool

OPENWEATHER_API_KEY = "6181bebdae59b62fa021aa4b0474bc85"

@tool
def get_forecast(city: str):
    """
    Get 5-day weather forecast with 3-hour intervals using OpenWeatherMap API with optimized networking.
    
    Args:
        city (str): Name of the city to get forecast data for
        
    Returns:
        dict: JSON response containing forecast data or error information.
              Uses connection pooling and has a 5-second timeout for better performance.
    
    Raises:
        RequestException: For network-related errors
        Exception: For other unexpected errors
    """
    try:
        # Use connection pooling and timeout
        session = requests.Session()
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = session.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}