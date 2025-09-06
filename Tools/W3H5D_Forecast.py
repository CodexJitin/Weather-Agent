import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from langchain_core.tools import tool

OPENWEATHER_API_KEY = "6181bebdae59b62fa021aa4b0474bc85"

# Configure a session with retry strategy
session = requests.Session()
retries = Retry(
    total=3,                # total retry attempts
    backoff_factor=0.5,     # wait time between retries: 0.5s, 1s, 2s...
    status_forcelist=[502, 503, 504, 524],  # retry on these HTTP codes
    allowed_methods=["GET"] # only retry GET requests
)
adapter = HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

@tool
def get_forecast(city: str):
    """
    Get 5-day weather forecast with 3-hour intervals using OpenWeatherMap API.
    Uses retries and extended timeouts for resilience.
    
    Args:
        city (str): Name of the city to get forecast data for.
        
    Returns:
        dict: JSON response containing forecast data or error information.
    """
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        # timeout=(connect_timeout, read_timeout)
        response = session.get(url, timeout=(3, 10))
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
