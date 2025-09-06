import requests
from langchain_core.tools import tool

@tool
def Current_location():
    """
    Get the current location based on IP address using ipinfo.io with optimized networking.
    
    Returns:
        dict: A dictionary containing location information with keys:
            - latitude (float): The location's latitude
            - longitude (float): The location's longitude
            - city (str): The city name
            - region (str): The region/state name
            - country (str): The country name
        None: If location data is unavailable or in case of errors
    """
    try:
        # Use connection pooling and timeout
        session = requests.Session()
        response = session.get("https://ipinfo.io/json", timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Fast path for missing location data
        loc = data.get("loc")
        if not loc:
            return None
            
        lat, lon = loc.split(",")
        return {
            "latitude": float(lat),
            "longitude": float(lon),
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country")
        }
    except Exception as e:
        print("Error getting location:", e)
        return None
