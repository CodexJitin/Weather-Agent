"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from langchain_core.language_models.base import BaseLanguageModel


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the LLM provider with configuration.
        
        Args:
            config: Configuration dictionary containing provider-specific settings
        """
        self.config = config
        self._llm: Optional[BaseLanguageModel] = None
    
    @abstractmethod
    def create_llm(self) -> BaseLanguageModel:
        """Create and return an LLM instance.
        
        Returns:
            Configured LLM instance
        """
        pass
    
    @property
    def llm(self) -> BaseLanguageModel:
        """Get the LLM instance, creating it if necessary.
        
        Returns:
            LLM instance
        """
        if self._llm is None:
            self._llm = self.create_llm()
        return self._llm
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the provider configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Get the provider name.
        
        Returns:
            Provider name
        """
        pass