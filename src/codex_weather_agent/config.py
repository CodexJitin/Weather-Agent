"""Configuration management for the Weather Agent."""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class WeatherAgentConfig:
    """Configuration class for the Weather Agent."""
    
    # LLM Configuration
    llm_provider: str = "openai"
    llm_config: Dict[str, Any] = field(default_factory=dict)
    
    # Weather API Configuration
    openweather_api_key: str = field(default_factory=lambda: os.getenv("OPENWEATHER_API_KEY", ""))
    
    # CLI Configuration
    enable_typing_effect: bool = True
    typing_delay: float = 0.02
    
    def __post_init__(self):
        """Post-initialization to load default LLM configurations."""
        if not self.llm_config:
            self.llm_config = self._get_default_llm_config()
    
    def _get_default_llm_config(self) -> Dict[str, Any]:
        """Get default LLM configuration based on provider."""
        base_config = {
            "temperature": 0,
            "timeout": 60,
        }
        
        if self.llm_provider == "openai":
            return {
                **base_config,
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            }
        elif self.llm_provider == "azure":
            return {
                **base_config,
                "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
                "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
                "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
                "model": os.getenv("AZURE_OPENAI_MODEL", "gpt-35-turbo"),
            }
        elif self.llm_provider == "gemini":
            return {
                **base_config,
                "api_key": os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"),
                "model": os.getenv("GEMINI_MODEL", "gemini-pro"),
            }
        elif self.llm_provider == "claude":
            return {
                **base_config,
                "api_key": os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY"),
                "model": os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229"),
            }
        else:
            return base_config
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "WeatherAgentConfig":
        """Create config from dictionary."""
        return cls(**config_dict)
    
    @classmethod
    def from_env(cls, llm_provider: Optional[str] = None) -> "WeatherAgentConfig":
        """Create config from environment variables."""
        provider = llm_provider or os.getenv("LLM_PROVIDER", "openai")
        return cls(llm_provider=provider)
    
    def update_llm_config(self, **kwargs) -> None:
        """Update LLM configuration with additional parameters."""
        self.llm_config.update(kwargs)
    
    def validate(self) -> bool:
        """Validate the configuration."""
        # Check if OpenWeather API key is provided
        if not self.openweather_api_key:
            return False
        
        # Check if LLM configuration has required keys based on provider
        if self.llm_provider == "openai":
            return bool(self.llm_config.get("api_key"))
        elif self.llm_provider == "azure":
            required = ["api_key", "azure_endpoint", "deployment_name"]
            return all(self.llm_config.get(key) for key in required)
        elif self.llm_provider == "gemini":
            return bool(self.llm_config.get("api_key"))
        elif self.llm_provider == "claude":
            return bool(self.llm_config.get("api_key"))
        
        return True