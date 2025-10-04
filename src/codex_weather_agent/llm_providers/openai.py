"""OpenAI LLM provider."""

from typing import Any, Dict
from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai import ChatOpenAI
from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def create_llm(self) -> BaseLanguageModel:
        """Create and return an OpenAI LLM instance.
        
        Returns:
            Configured OpenAI LLM instance
        """
        # Support both openai_api_key and api_key for flexibility
        api_key = self.config.get("api_key") or self.config.get("openai_api_key")
        model_name = self.config.get("model") or self.config.get("model_name", "gpt-3.5-turbo")
        
        return ChatOpenAI(
            api_key=api_key,
            model=model_name,
            temperature=self.config.get("temperature", 0),
            max_tokens=self.config.get("max_tokens"),
            timeout=self.config.get("timeout", 60),
        )
    
    def validate_config(self) -> bool:
        """Validate the OpenAI configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Check for API key with multiple possible names
        api_key = self.config.get("api_key") or self.config.get("openai_api_key")
        
        # If no API key provided, check environment variables
        if not api_key:
            import os
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.config["api_key"] = api_key
                
        return api_key is not None
    
    @property
    def provider_name(self) -> str:
        """Get the provider name.
        
        Returns:
            Provider name
        """
        return "openai"