"""
Custom exceptions for the Codex Weather Agent package.
"""


class WeatherAgentError(Exception):
    """Base exception class for weather agent errors."""
    pass


class LLMConfigError(WeatherAgentError):
    """Raised when there's an issue with LLM configuration."""
    pass


class APIKeyError(WeatherAgentError):
    """Raised when API key is missing or invalid."""
    pass


class WeatherAPIError(WeatherAgentError):
    """Raised when weather API calls fail."""
    pass


class MemoryError(WeatherAgentError):
    """Raised when there are issues with conversation memory."""
    pass