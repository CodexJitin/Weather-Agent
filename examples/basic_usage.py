#!/usr/bin/env python3
"""
Basic usage example for the Codex Weather Agent.

This example demonstrates how to use the Weather Agent in a production environment
with proper error handling and logging.
"""

import logging
import sys
from codex_weather_agent import WeatherAgent, WeatherAgentConfig
from codex_weather_agent.logging_config import setup_logging


def main():
    """Main example function."""
    # Set up logging
    setup_logging(level="INFO")
    logger = logging.getLogger(__name__)
    
    try:
        # Create agent with default OpenAI provider
        logger.info("Creating Weather Agent...")
        agent = WeatherAgent(provider_name="openai")
        
        # Example queries
        queries = [
            "What's the weather like in New York?",
            "Will it rain tomorrow in London?",
            "What's the temperature in Tokyo right now?",
            "Is it sunny in San Francisco?"
        ]
        
        for query in queries:
            try:
                logger.info(f"Processing query: {query}")
                response = agent.query(query)
                print(f"\n🌤️  Query: {query}")
                print(f"📊 Response: {response}")
                print("-" * 60)
                
            except Exception as e:
                logger.error(f"Error processing query '{query}': {e}")
                print(f"❌ Error: {e}")
                
    except Exception as e:
        logger.error(f"Failed to initialize Weather Agent: {e}")
        print(f"❌ Initialization error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()