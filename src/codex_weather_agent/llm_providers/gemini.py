"""Google Gemini LLM provider."""

from typing import Any, Dict
from langchain_core.language_models.base import BaseLanguageModel
from langchain_google_genai import ChatGoogleGenerativeAI
from .base import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider."""
    
    def create_llm(self) -> BaseLanguageModel:
        """Create and return a Gemini LLM instance.
        
        Returns:
            Configured Gemini LLM instance
        """
        # Support multiple key names for flexibility
        api_key = self.config.get("api_key") or self.config.get("google_api_key") or self.config.get("gemini_api_key")
        model_name = self.config.get("model") or self.config.get("model_name", "gemini-2.5-flash")
        
        return ChatGoogleGenerativeAI(
            google_api_key=api_key,
            model=model_name,
            temperature=self.config.get("temperature", 0),
            max_output_tokens=self.config.get("max_tokens"),
            timeout=self.config.get("timeout", 60),
        )
    
    def validate_config(self) -> bool:
        """Validate the Gemini configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Check for API key with multiple possible names
        api_key = (self.config.get("api_key") or 
                  self.config.get("google_api_key") or 
                  self.config.get("gemini_api_key"))
        return api_key is not None
    
    @property
    def provider_name(self) -> str:
        """Get the provider name.
        
        Returns:
            Provider name
        """
        return "gemini"