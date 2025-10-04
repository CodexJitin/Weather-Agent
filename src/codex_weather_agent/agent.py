"""Main weather agent class."""

import logging
from typing import Dict, Any, Optional
from .workflow import WeatherAgentWorkflow
from .llm_providers.factory import create_llm_provider
from .llm_providers.base import LLMProvider
from .config import WeatherAgentConfig

logger = logging.getLogger(__name__)


class WeatherAgent:
    """Main weather agent class that orchestrates the LangGraph workflow."""
    
    def __init__(self, 
                 provider_name: str = "openai",
                 provider_config: Optional[Dict[str, Any]] = None,
                 openweather_api_key: Optional[str] = None):
        """Initialize the weather agent.
        
        Args:
            provider_name: Name of the LLM provider ("openai", "azure", "gemini", "claude")
            provider_config: Configuration for the LLM provider
            openweather_api_key: OpenWeatherMap API key (optional, uses environment variable if not provided)
            
        Raises:
            ValueError: If the provider configuration is invalid
            RuntimeError: If initialization fails
        """
        if provider_config is None:
            provider_config = {}
            
        try:
            # If no OpenWeather API key provided, try to get it from environment
            if openweather_api_key is None:
                config = WeatherAgentConfig.from_env(provider_name)
                openweather_api_key = config.openweather_api_key
                
            if not openweather_api_key:
                raise ValueError("OpenWeatherMap API key is required")
                
            logger.info(f"Initializing Weather Agent with provider: {provider_name}")
            self.llm_provider = create_llm_provider(provider_name, provider_config)
            self.openweather_api_key = openweather_api_key
            self.workflow = WeatherAgentWorkflow(self.llm_provider, self.openweather_api_key)
            logger.info("Weather Agent initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Weather Agent: {e}")
            raise RuntimeError(f"Weather Agent initialization failed: {e}") from e
    
    @classmethod
    def from_config(cls, config: WeatherAgentConfig) -> "WeatherAgent":
        """Create agent from configuration object.
        
        Args:
            config: WeatherAgentConfig instance
            
        Returns:
            WeatherAgent instance
        """
        return cls(
            provider_name=config.llm_provider,
            provider_config=config.llm_config,
            openweather_api_key=config.openweather_api_key
        )
    
    def query(self, user_input: str) -> str:
        """Process a weather query.
        
        Args:
            user_input: User's weather query
            
        Returns:
            Weather assistant's response
            
        Raises:
            ValueError: If user_input is empty or invalid
            RuntimeError: If the workflow processing fails
        """
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty")
            
        try:
            logger.info(f"Processing weather query: {user_input[:50]}...")
            response = self.workflow.process_query(user_input)
            logger.info("Query processed successfully")
            return response
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise RuntimeError(f"Failed to process weather query: {e}") from e
    
    @property
    def supported_providers(self) -> list:
        """Get list of supported LLM providers."""
        from .llm_providers.factory import create_llm_provider
        
        # Test which providers are available
        providers = ["openai", "azure"]
        
        # Check optional providers
        try:
            from .llm_providers.gemini import GeminiProvider
            providers.append("gemini")
        except ImportError:
            pass
            
        try:
            from .llm_providers.claude import ClaudeProvider
            providers.append("claude")
        except ImportError:
            pass
            
        return providers

    def get_provider_info(self) -> Dict[str, str]:
        """Get information about the current LLM provider.
        
        Returns:
            Dictionary with provider information
        """
        return {
            "provider_name": self.llm_provider.provider_name,
            "model_info": str(self.llm_provider.llm),
        }