"""Azure OpenAI LLM provider."""

from typing import Any, Dict
from langchain_core.language_models.base import BaseLanguageModel
from langchain_openai import AzureChatOpenAI
from .base import LLMProvider


class AzureOpenAIProvider(LLMProvider):
    """Azure OpenAI LLM provider."""
    
    def create_llm(self) -> BaseLanguageModel:
        """Create and return an Azure OpenAI LLM instance.
        
        Returns:
            Configured Azure OpenAI LLM instance
        """
        # Support multiple key names for flexibility
        api_key = self.config.get("api_key") or self.config.get("azure_openai_api_key")
        model_name = self.config.get("model") or self.config.get("model_name", "gpt-35-turbo")
        
        return AzureChatOpenAI(
            api_key=api_key,
            azure_endpoint=self.config.get("azure_endpoint"),
            api_version=self.config.get("api_version", "2024-02-01"),
            deployment_name=self.config.get("deployment_name"),
            model=model_name,
            temperature=self.config.get("temperature", 0),
            max_tokens=self.config.get("max_tokens"),
            timeout=self.config.get("timeout", 60),
        )
    
    def validate_config(self) -> bool:
        """Validate the Azure OpenAI configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        # Check for API key with multiple possible names
        api_key = self.config.get("api_key") or self.config.get("azure_openai_api_key")
        azure_endpoint = self.config.get("azure_endpoint")
        deployment_name = self.config.get("deployment_name")
        
        return all([api_key, azure_endpoint, deployment_name])
    
    @property
    def provider_name(self) -> str:
        """Get the provider name.
        
        Returns:
            Provider name
        """
        return "azure"