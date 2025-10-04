"""Anthropic Claude LLM provider."""

from typing import Any, Dict
from langchain_core.language_models.base import BaseLanguageModel
from langchain_anthropic import ChatAnthropic
from .base import LLMProvider


class ClaudeProvider(LLMProvider):
    """Anthropic Claude LLM provider."""
    
    def create_llm(self) -> BaseLanguageModel:
        """Create and return a Claude LLM instance.
        
        Returns:
            Configured Claude LLM instance
        """
        # Support multiple key names for flexibility
        api_key = self.config.get("api_key") or self.config.get("anthropic_api_key") or self.config.get("claude_api_key")
        model_name = self.config.get("model") or self.config.get("model_name", "claude-3-sonnet-20240229")
        
        return ChatAnthropic(
            anthropic_api_key=api_key,
            model=model_name,
            temperature=self.config.get("temperature", 0),
            max_tokens=self.config.get("max_tokens", 1024),
            timeout=self.config.get("timeout", 60),
        )
    
    def validate_config(self) -> bool:
        """Validate the Claude configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Check for API key with multiple possible names
        api_key = (self.config.get("api_key") or 
                  self.config.get("anthropic_api_key") or 
                  self.config.get("claude_api_key"))
        return api_key is not None
    
    @property
    def provider_name(self) -> str:
        """Get the provider name.
        
        Returns:
            Provider name
        """
        return "claude"