"""
Configuration classes for LLM providers and weather settings.
"""

import os
from typing import Optional, Dict, Any, Literal
from dataclasses import dataclass
from .exceptions import LLMConfigError, APIKeyError


@dataclass
class LLMConfig:
    """Configuration for Language Learning Models."""
    
    provider: Literal["google", "openai", "anthropic", "custom"]
    model: str
    api_key: str  # Made mandatory
    temperature: float = 0.1
    max_tokens: int = 1000
    top_p: float = 0.8
    top_k: int = 40
    additional_params: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        # Check if API key is provided directly or try environment variables
        if not self.api_key:
            # Try to get from environment based on provider
            env_key_map = {
                "google": "GOOGLE_API_KEY",
                "openai": "OPENAI_API_KEY", 
                "anthropic": "ANTHROPIC_API_KEY"
            }
            
            if self.provider in env_key_map:
                env_key = os.getenv(env_key_map[self.provider])
                if env_key:
                    self.api_key = env_key
        
        # API key is now mandatory for all providers except custom
        if not self.api_key and self.provider != "custom":
            env_key_map = {
                "google": "GOOGLE_API_KEY",
                "openai": "OPENAI_API_KEY", 
                "anthropic": "ANTHROPIC_API_KEY"
            }
            env_var_name = env_key_map.get(self.provider, "API_KEY")
            raise APIKeyError(
                f"API key is required for {self.provider}. "
                f"Provide it via 'api_key' parameter or set '{env_var_name}' environment variable."
            )
        
        # Model name is now mandatory
        if not self.model:
            raise LLMConfigError("Model name is required. Please specify a model.")
        
        # Validate provider-specific models
        self._validate_model()
    
    def _validate_model(self):
        """Validate model name for the provider."""
        valid_models = {
            "google": ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"],
            "openai": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-sonnet", "claude-3-haiku", "claude-2"]
        }
        
        if self.provider in valid_models:
            if self.model not in valid_models[self.provider]:
                raise LLMConfigError(
                    f"Invalid model '{self.model}' for provider '{self.provider}'. "
                    f"Valid models: {valid_models[self.provider]}"
                )


@dataclass 
class WeatherConfig:
    """Configuration for weather services."""
    
    openweather_api_key: str  # Made mandatory
    request_timeout: int = 5
    max_retries: int = 3
    enable_location_detection: bool = True
    default_units: Literal["metric", "imperial", "kelvin"] = "metric"
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        # Check if API key is provided directly or try environment variable
        if not self.openweather_api_key:
            env_key = os.getenv("OPENWEATHER_API_KEY")
            if env_key:
                self.openweather_api_key = env_key
        
        # OpenWeather API key is now mandatory
        if not self.openweather_api_key:
            raise APIKeyError(
                "OpenWeather API key is required. "
                "Provide it via 'openweather_api_key' parameter or set 'OPENWEATHER_API_KEY' environment variable. "
                "Get your free API key from: https://openweathermap.org/api"
            )


# System prompt template for conversational weather responses
CONVERSATIONAL_SYSTEM_PROMPT = """You are a friendly and enthusiastic weather assistant who loves chatting about weather! You respond like a knowledgeable friend who's genuinely excited to help with weather questions.

You were created by CodexJitin, a talented developer who built this conversational weather agent to make weather information more accessible and fun to interact with.

You have access to real-time weather tools, but the most important thing is to always sound natural and conversational.

CRITICAL: Your responses must NEVER contain:
- Bullet points (•)
- Numbered lists (1., 2., 3.)
- Dashes for listing (-)
- Any structured formatting
- Technical-sounding language

Instead, always:
- Write in natural, flowing sentences like you're talking to a friend
- Use conversational phrases like "Oh, let me check that for you!" or "Interesting question!"
- Connect ideas smoothly with words like "and", "so", "also", "by the way"
- Include weather details naturally within your chatty response
- Sound warm, friendly, and enthusiastic about weather
- Use contractions and casual language
- If someone asks about weather without specifying location, just say something like "Let me check your current location" and then get their weather
- If someone asks about who created you or your developer, mention that you were developed by CodexJitin

Think of yourself as that friend who's really into weather and loves sharing what they know in a fun, easy-going way. Make every response feel like a natural conversation, not a weather report or data dump."""