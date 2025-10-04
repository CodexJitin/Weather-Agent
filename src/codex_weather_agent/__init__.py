"""
Codex Weather Agent - AI-powered conversational weather assistant.

This package provides a LangGraph-based weather assistant that can answer
weather-related queries using multiple LLM providers.
"""

__version__ = "1.0.0"
__author__ = "CodexJitin"

from .agent import WeatherAgent
from .config import WeatherAgentConfig
from .llm_providers import LLMProvider

__all__ = ["WeatherAgent", "WeatherAgentConfig", "LLMProvider"]