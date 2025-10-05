import requests
from langchain_core.tools import tool
from typing import Optional, Dict, Any

# Configuration
IPINFO_URL = "https://ipinfo.io/json"


@tool
def current_location() -> Optional[Dict[str, Any]]:
    """
    Get the current location based on IP address using ipinfo.io with optimized networking.
    
    Returns:
        Optional[Dict[str, Any]]: A dictionary containing location information with keys:
            - latitude (float): The location's latitude
            - longitude (float): The location's longitude  
            - city (str): The city name
            - region (str): The region/state name
            - country (str): The country name
        Returns None if location data is unavailable or in case of errors
    """
    try:
        # Use optimized session with connection pooling
        with requests.Session() as session:
            response = session.get(IPINFO_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
        
        # Fast path for missing location data
        loc = data.get("loc")
        if not loc:
            return None
            
        # Parse coordinates efficiently
        lat, lon = map(float, loc.split(","))
        
        return {
            "latitude": lat,
            "longitude": lon,
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country")
        }
    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Error getting location: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error getting location: {e}")
        return None