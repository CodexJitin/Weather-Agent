"""LLM provider factory."""

from typing import Any, Dict
from .base import LLMProvider
from .openai import OpenAIProvider
from .azure import AzureOpenAIProvider

# Import optional providers
try:
    from .gemini import GeminiProvider
except ImportError:
    GeminiProvider = None

try:
    from .claude import ClaudeProvider
except ImportError:
    ClaudeProvider = None


def create_llm_provider(provider_name: str, config: Dict[str, Any]) -> LLMProvider:
    """Create an LLM provider instance.
    
    Args:
        provider_name: Name of the provider ("openai", "azure", "gemini", "claude")
        config: Configuration dictionary for the provider
        
    Returns:
        LLM provider instance
        
    Raises:
        ValueError: If provider_name is not supported
    """
    providers = {
        "openai": OpenAIProvider,
        "azure": AzureOpenAIProvider,
    }
    
    # Add optional providers if available
    if GeminiProvider is not None:
        providers["gemini"] = GeminiProvider
    if ClaudeProvider is not None:
        providers["claude"] = ClaudeProvider
    
    if provider_name not in providers:
        supported = ", ".join(providers.keys())
        raise ValueError(f"Unsupported provider: {provider_name}. Supported providers: {supported}")
    
    provider_class = providers[provider_name]
    provider = provider_class(config)
    
    if not provider.validate_config():
        raise ValueError(f"Invalid configuration for provider: {provider_name}")
    
    return provider