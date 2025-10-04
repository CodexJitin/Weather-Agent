"""Current location detection tool for LangGraph with optimized performance."""

import logging
import requests
from typing import Dict, Any, Optional
from functools import lru_cache
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Use a separate session for IP geolocation (different service)
_location_session: Optional[requests.Session] = None

def get_location_session() -> requests.Session:
    """Get a reusable session for location detection."""
    global _location_session
    if _location_session is None:
        _location_session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=5,
            pool_maxsize=10
        )
        _location_session.mount("http://", adapter)
        _location_session.mount("https://", adapter)
    return _location_session

@lru_cache(maxsize=1)  # Cache the user's location (typically doesn't change often)
def _get_cached_location() -> Optional[Dict[str, Any]]:
    """Get and cache the current location based on IP."""
    try:
        session = get_location_session()
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
    return _get_cached_location()