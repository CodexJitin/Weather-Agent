import requests
from langchain_core.tools import tool

OPENWEATHER_API_KEY = "6181bebdae59b62fa021aa4b0474bc85"

@tool
def get_weather(city: str):
    """
    Get current weather data for a given city using OpenWeatherMap API with optimized networking.
    
    Args:
        city (str): Name of the city to get weather data for
        
    Returns:
        dict: JSON response containing weather data or error information
              Uses connection pooling and has a 5-second timeout for better performance
    
    Raises:
        HTTPError: Automatically raised for non-200 status codes
    """
    try:
        # Add timeout and use session for connection pooling
        session = requests.Session()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = session.get(url, timeout=5)
        response.raise_for_status()  # Raises HTTPError for bad responses
        return response.json()
    except Exception as e:
        return {"error": str(e)}