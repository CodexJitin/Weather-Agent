"""LLM providers package."""

from .base import LLMProvider
from .openai import OpenAIProvider
from .azure import AzureOpenAIProvider
from .factory import create_llm_provider

# Import optional providers with graceful fallback
try:
    from .gemini import GeminiProvider
except ImportError:
    GeminiProvider = None

try:
    from .claude import ClaudeProvider
except ImportError:
    ClaudeProvider = None

__all__ = [
    "LLMProvider",
    "OpenAIProvider", 
    "AzureOpenAIProvider",
    "GeminiProvider",
    "ClaudeProvider",
    "create_llm_provider",
]