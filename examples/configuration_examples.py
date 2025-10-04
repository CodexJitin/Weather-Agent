#!/usr/bin/env python3
"""
Configuration examples for the Codex Weather Agent.

This example demonstrates different ways to configure the weather agent
for various deployment scenarios and LLM providers.
"""

import os
import logging
from codex_weather_agent import WeatherAgent, WeatherAgentConfig
from codex_weather_agent.logging_config import setup_logging


def example_basic_configuration():
    """Example: Basic configuration with environment variables."""
    print("=== Basic Configuration ===")
    
    # Set up environment variables (typically done in deployment)
    # os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    # os.environ["OPENWEATHER_API_KEY"] = "your-openweather-api-key"
    
    try:
        # Create agent with minimal configuration
        agent = WeatherAgent(provider_name="openai")
        
        response = agent.query("What's the weather in New York?")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure API keys are set in environment variables")


def example_direct_configuration():
    """Example: Direct API key configuration."""
    print("\n=== Direct Configuration ===")
    
    try:
        # Configure with direct API keys
        agent = WeatherAgent(
            provider_name="openai",
            provider_config={
                "api_key": "your-openai-api-key-here",
                "model": "gpt-4",
                "temperature": 0.1
            },
            openweather_api_key="your-openweather-api-key-here"
        )
        
        response = agent.query("Will it rain tomorrow in London?")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")


def example_config_object():
    """Example: Using WeatherAgentConfig object."""
    print("\n=== Configuration Object ===")
    
    try:
        # Create configuration object
        config = WeatherAgentConfig(
            llm_provider="openai",
            openweather_api_key=os.getenv("OPENWEATHER_API_KEY", "your-key-here")
        )
        
        # Update LLM configuration
        config.update_llm_config(
            api_key=os.getenv("OPENAI_API_KEY", "your-key-here"),
            model="gpt-3.5-turbo",
            temperature=0.0,
            max_tokens=1000
        )
        
        # Validate configuration
        if config.validate():
            agent = WeatherAgent.from_config(config)
            response = agent.query("What's the temperature in Tokyo?")
            print(f"Response: {response}")
        else:
            print("Configuration validation failed")
            
    except Exception as e:
        print(f"Error: {e}")


def example_multiple_providers():
    """Example: Testing multiple LLM providers."""
    print("\n=== Multiple Providers ===")
    
    providers = {
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "model": "gpt-3.5-turbo"
        },
        "azure": {
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "deployment_name": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        },
        "gemini": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "model": "gemini-pro"
        },
        "claude": {
            "api_key": os.getenv("ANTHROPIC_API_KEY"),
            "model": "claude-3-sonnet-20240229"
        }
    }
    
    for provider_name, config in providers.items():
        if config.get("api_key"):
            try:
                print(f"\nTesting {provider_name.upper()}...")
                agent = WeatherAgent(
                    provider_name=provider_name,
                    provider_config=config
                )
                
                response = agent.query("Is it sunny in California?")
                print(f"Response: {response[:100]}...")
                
            except Exception as e:
                print(f"Error with {provider_name}: {e}")
        else:
            print(f"\nSkipping {provider_name} - no API key")


def example_production_configuration():
    """Example: Production-ready configuration with logging."""
    print("\n=== Production Configuration ===")
    
    # Set up production logging
    setup_logging(level="INFO", enable_debug=False)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration from environment
        config = WeatherAgentConfig.from_env("openai")
        
        # Validate before creating agent
        if not config.validate():
            raise ValueError("Invalid configuration")
            
        # Create agent
        agent = WeatherAgent.from_config(config)
        
        # Get provider information for monitoring
        provider_info = agent.get_provider_info()
        logger.info(f"Using provider: {provider_info}")
        
        # Process query with error handling
        query = "What's the weather forecast for the next 3 days in Paris?"
        response = agent.query(query)
        
        print(f"Query: {query}")
        print(f"Response: {response}")
        
    except Exception as e:
        logger.error(f"Production example failed: {e}")
        print(f"Error: {e}")


def main():
    """Run all configuration examples."""
    print("Codex Weather Agent - Configuration Examples")
    print("=" * 50)
    
    example_basic_configuration()
    example_direct_configuration()
    example_config_object()
    example_multiple_providers()
    example_production_configuration()
    
    print("\n" + "=" * 50)
    print("Configuration Examples Complete")
    print("For production use, set environment variables:")
    print("- OPENAI_API_KEY (or your chosen LLM provider key)")
    print("- OPENWEATHER_API_KEY")


if __name__ == "__main__":
    main()
    
    print(f"Created sample config file: {config_path}")
    
    # Load configuration
    config = WeatherAgentConfig(str(config_path))
    provider = config.get_llm_provider()
    provider_config = config.get_llm_config(provider)
    
    print(f"Loaded provider: {provider}")
    print(f"Provider config: {provider_config}")
    
    # Clean up
    config_path.unlink()

def config_with_env_vars():
    """Example: Using environment variables."""
    
    # Set environment variables (in practice, you'd set these in your shell or .env file)
    os.environ["WEATHER_AGENT_LLM_PROVIDER"] = "openai"
    os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
    os.environ["OPENAI_MODEL"] = "gpt-4"
    
    # Load configuration
    config = WeatherAgentConfig()
    provider = config.get_llm_provider()
    provider_config = config.get_llm_config(provider)
    
    print(f"Provider from env: {provider}")
    print(f"Config from env: {provider_config}")

def config_template_example():
    """Example: Get configuration template."""
    
    config = WeatherAgentConfig()
    template = config.get_config_template()
    
    print("Configuration template:")
    print(json.dumps(template, indent=2))

def multi_provider_example():
    """Example: Using multiple providers."""
    
    providers_config = {
        "openai": {
            "api_key": os.getenv("OPENAI_API_KEY", "fake_key"),
            "model": "gpt-3.5-turbo"
        },
        "gemini": {
            "api_key": os.getenv("GOOGLE_API_KEY", "fake_key"),
            "model": "gemini-pro"
        }
    }
    
    for provider_name, config in providers_config.items():
        print(f"\n=== {provider_name.upper()} Configuration ===")
        try:
            agent = WeatherAgent(provider_name, config)
            info = agent.get_provider_info()
            print(f"Provider: {info['provider_name']}")
            print(f"Model info: {info['model_info']}")
        except Exception as e:
            print(f"Failed to initialize {provider_name}: {e}")

def main():
    """Run configuration examples."""
    print("=== Configuration Examples ===\n")
    
    print("1. Configuration with file:")
    config_with_file()
    
    print("\n2. Configuration with environment variables:")
    config_with_env_vars()
    
    print("\n3. Configuration template:")
    config_template_example()
    
    print("\n4. Multi-provider example:")
    multi_provider_example()

if __name__ == "__main__":
    main()