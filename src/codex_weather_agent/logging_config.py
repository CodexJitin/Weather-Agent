"""Logging configuration for the Weather Agent."""

import logging
import logging.config
from typing import Optional


def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    enable_debug: bool = False
) -> None:
    """
    Set up logging configuration for the Weather Agent.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        enable_debug: Enable debug logging for external libraries
    """
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Suppress verbose logging from external libraries unless debug is enabled
    if not enable_debug:
        # Suppress HTTP request logs unless there are errors
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        
        # Suppress LangChain debug logs
        logging.getLogger("langchain").setLevel(logging.WARNING)
        logging.getLogger("langchain_core").setLevel(logging.WARNING)
        logging.getLogger("langchain_openai").setLevel(logging.WARNING)
        logging.getLogger("langchain_google_genai").setLevel(logging.WARNING)
        logging.getLogger("langchain_anthropic").setLevel(logging.WARNING)
        
        # Suppress LangGraph debug logs
        logging.getLogger("langgraph").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# Default logger for the package
logger = get_logger(__name__)