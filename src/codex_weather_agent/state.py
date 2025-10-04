"""Weather agent state definition."""

from typing import Dict, Any, List, Optional, TypedDict
from langchain_core.messages import BaseMessage


class WeatherAgentState(TypedDict):
    """State for the weather agent workflow."""
    
    # Input/Output
    query: str
    response: Optional[str]
    
    # Messages for LLM conversation
    messages: List[BaseMessage]
    
    # Tool execution tracking
    tool_calls: List[Dict[str, Any]]
    tool_results: List[Dict[str, Any]]
    
    # Location context
    current_location: Optional[Dict[str, Any]]
    target_location: Optional[str]
    coordinates: Optional[Dict[str, Any]]
    
    # Weather data
    weather_data: Optional[Dict[str, Any]]
    forecast_data: Optional[Dict[str, Any]]
    pollution_data: Optional[Dict[str, Any]]
    
    # Control flow
    next_action: Optional[str]
    error: Optional[str]
    is_complete: bool