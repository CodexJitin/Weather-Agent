"""
LLM Factory for creating different language model providers.
"""

from typing import Optional
from langchain_core.language_models import BaseChatModel

from .config import LLMConfig
from .exceptions import LLMConfigError, APIKeyError


def create_llm(config: LLMConfig) -> BaseChatModel:
    """
    Create an LLM instance based on the configuration.
    
    Args:
        config: LLM configuration
        
    Returns:
        BaseChatModel: Configured LLM instance
        
    Raises:
        LLMConfigError: If configuration is invalid
        APIKeyError: If API key is missing
    """
    if config.provider == "google":
        return _create_google_llm(config)
    elif config.provider == "openai":
        return _create_openai_llm(config)
    elif config.provider == "anthropic":
        return _create_anthropic_llm(config)
    else:
        raise LLMConfigError(f"Unsupported LLM provider: {config.provider}")


def _create_google_llm(config: LLMConfig) -> BaseChatModel:
    """Create Google Gemini LLM."""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError:
        raise LLMConfigError("langchain-google-genai is required for Google models. Install with: pip install langchain-google-genai")
    
    if not config.api_key:
        raise APIKeyError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
    
    params = {
        "model": config.model,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "google_api_key": config.api_key,
        "convert_system_message_to_human": True  # Gemini compatibility
    }
    
    # Add Google-specific parameters
    if hasattr(config, 'top_p'):
        params["top_p"] = config.top_p
    if hasattr(config, 'top_k'):
        params["top_k"] = config.top_k
    
    # Add any additional parameters
    if config.additional_params:
        params.update(config.additional_params)
    
    return ChatGoogleGenerativeAI(**params)


def _create_openai_llm(config: LLMConfig) -> BaseChatModel:
    """Create OpenAI LLM."""
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        raise LLMConfigError("langchain-openai is required for OpenAI models. Install with: pip install langchain-openai")
    
    if not config.api_key:
        raise APIKeyError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
    
    params = {
        "model": config.model,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "openai_api_key": config.api_key
    }
    
    # Add any additional parameters
    if config.additional_params:
        params.update(config.additional_params)
    
    return ChatOpenAI(**params)


def _create_anthropic_llm(config: LLMConfig) -> BaseChatModel:
    """Create Anthropic Claude LLM."""
    try:
        from langchain_anthropic import ChatAnthropic
    except ImportError:
        raise LLMConfigError("langchain-anthropic is required for Anthropic models. Install with: pip install langchain-anthropic")
    
    if not config.api_key:
        raise APIKeyError("Anthropic API key is required. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.")
    
    params = {
        "model": config.model,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "anthropic_api_key": config.api_key
    }
    
    # Add any additional parameters
    if config.additional_params:
        params.update(config.additional_params)
    
    return ChatAnthropic(**params)