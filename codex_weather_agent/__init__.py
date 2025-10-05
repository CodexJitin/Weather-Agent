"""
Codex Weather Agent - A conversational weather agent powered by LangGraph and LLMs

A Python package providing intelligent weather information through natural language
conversations with configurable LLM support and memory management.
"""

__version__ = "1.0.5"
__author__ = "CodexJitin"
__email__ = "contact@codexjitin.com"
__description__ = "Conversational weather agent with LangGraph and configurable LLMs"

from .agent import WeatherAgent, create_weather_agent
from .config import LLMConfig, WeatherConfig
from .exceptions import WeatherAgentError, LLMConfigError, APIKeyError

__all__ = [
    "WeatherAgent",
    "create_weather_agent", 
    "LLMConfig",
    "WeatherConfig",
    "WeatherAgentError",
    "LLMConfigError", 
    "APIKeyError",
    "__version__"
]