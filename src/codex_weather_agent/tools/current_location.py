"""Current location detection tool for LangGraph."""

import logging
import requests
from typing import Dict, Any, Optional
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

def _get_location() -> Optional[Dict[str, Any]]:
    """Get the current location based on IP."""
    try:
        response = requests.get("https://ipinfo.io/json", timeout=10)
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
        logger.warning(f"Error getting location: {e}")
        return None

@tool
def current_location() -> Optional[Dict[str, Any]]:
    """
    Get the current location based on IP address using ipinfo.io.
    
    Returns:
        Dictionary containing location information with keys:
        - latitude (float): The location's latitude
        - longitude (float): The location's longitude
        - city (str): The city name
        - region (str): The region/state name
        - country (str): The country name
        
        Returns None if location data is unavailable or in case of errors
    """
    return _get_location()