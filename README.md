# 🌤️ Codex Weather Agent

[![PyPI version](https://badge.fury.io/py/codex-weather-agent.svg)](https://badge.fury.io/py/codex-weather-agent)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A **professional conversational weather service** built with [LangGraph](https://www.langchain.com/langgraph), supporting multiple LLM providers (OpenAI, Azure OpenAI, Gemini, Claude) and providing real-time weather data through a production-ready Python API.

## ✨ Features

- 🤖 **Natural Conversations**: Intuitive natural language interactions powered by LangGraph workflows
- 🌍 **Multiple LLM Support**: OpenAI, Azure OpenAI, Google Gemini, and Anthropic Claude
- 🌦️ **Comprehensive Weather Data**: Current conditions, forecasts, and air quality
- 📍 **Location Intelligence**: Automatic location detection and coordinate lookup
- ⚙️ **Flexible Configuration**: Environment variables and programmatic setup
- 🔧 **Easy Integration**: Production-ready Python library for applications
- 📊 **Proper Logging**: Structured logging with configurable levels
- 🛡️ **Error Handling**: Robust error handling and validation

## 🚀 Installation

### From PyPI

```bash
pip install codex-weather-agent
```

### From Source

```bash
git clone https://github.com/CodexJitin/Weather-Agent.git
cd Weather-Agent
pip install -e .
```

## ⚙️ Configuration

### 1. Get API Keys

You'll need:
- **OpenWeatherMap API Key**: [Get it here](https://openweathermap.org/api) (Required)
- **LLM Provider API Key**: Choose from OpenAI, Azure OpenAI, Google Gemini, or Anthropic Claude

### 2. Environment Setup

Create a `.env` file (copy from `.env.example`):

```bash
# Weather API (Required)  
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Choose your LLM provider
LLM_PROVIDER=openai

# OpenAI (default)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Or Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
AZURE_OPENAI_MODEL=gpt-35-turbo

# Or Google Gemini
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-pro

# Or Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here
CLAUDE_MODEL=claude-3-sonnet-20240229
```

## 🎯 Usage

### Basic Library Usage

```python
from codex_weather_agent import WeatherAgent
from codex_weather_agent.logging_config import setup_logging

# Set up logging (optional)
setup_logging(level="INFO")

# Method 1: Use environment variables (recommended)
agent = WeatherAgent(provider_name="openai")
response = agent.query("What's the weather in Tokyo?")
print(response)

# Method 2: Pass API keys directly
agent = WeatherAgent(
    provider_name="openai",
    provider_config={
        "api_key": "your-openai-api-key",
        "model": "gpt-4"
    },
    openweather_api_key="your-openweather-api-key"
)

# Method 3: Use configuration object
from codex_weather_agent import WeatherAgentConfig

config = WeatherAgentConfig(
    llm_provider="openai",
    openweather_api_key="your-openweather-api-key"
)
config.update_llm_config(api_key="your-openai-api-key", model="gpt-4")
agent = WeatherAgent.from_config(config)
response = agent.query("Air quality in Delhi?")
```

### Advanced Configuration

```python
from weather_agent_langgraph import WeatherAgent

# Configure different LLM providers
configs = {
    "openai": {
        "api_key": "sk-...",
        "model": "gpt-4",
        "temperature": 0
    },
    "azure": {
        "api_key": "your-key",
        "azure_endpoint": "https://your-resource.openai.azure.com/",
        "deployment_name": "gpt-35-turbo",
        "model": "gpt-35-turbo"
    },
    "gemini": {
        "api_key": "your-google-key",
        "model": "gemini-pro"
    },
    "claude": {
        "api_key": "your-anthropic-key", 
        "model": "claude-3-sonnet-20240229"
    }
}

# Create agent with specific provider
agent = WeatherAgent(
    provider_name="gemini",
    provider_config=configs["gemini"]
)
```

## 🌟 Example Queries

The agent understands natural language queries:

- "What's the weather in New York?"
- "Give me the air quality for Delhi"
- "5-day forecast for London"
- "Is it raining in my location?"
- "Compare weather between Tokyo and Paris"
- "What should I wear in Mumbai today?"

## 🏗️ Architecture

The package uses a **LangGraph workflow** with the following components:

- **Agent**: Main orchestrator class
- **Workflow**: LangGraph state machine for query processing
- **Tools**: Weather data collection (OpenWeatherMap API)
- **LLM Providers**: Abstraction layer for different AI models
- **State Management**: Conversation and tool execution tracking

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query    │───▶│  LangGraph       │───▶│   AI Response   │
│                 │    │  Workflow        │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Weather Tools   │
                    │  • Current       │
                    │  • Forecast      │
                    │  • Air Quality   │
                    │  • Location      │
                    └──────────────────┘
```

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/CodexJitin/Codex-Weather-Agent.git
cd Codex-Weather-Agent

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
isort src/
```

## 📋 Requirements

- Python 3.8+
- OpenWeatherMap API key
- One of the supported LLM provider API keys:
  - OpenAI API key
  - Azure OpenAI credentials
  - Google AI Studio API key (for Gemini)
  - Anthropic API key (for Claude)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://www.langchain.com/) and [LangGraph](https://python.langchain.com/docs/langgraph) for the AI framework
- [OpenWeatherMap](https://openweathermap.org/) for weather data
- [Rich](https://github.com/Textualize/rich) for beautiful CLI interfaces

## 📞 Support

- 📫 **Issues**: [GitHub Issues](https://github.com/CodexJitin/Codex-Weather-Agent/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/CodexJitin/Codex-Weather-Agent/discussions)

---

<p align="center">
  <strong>🌤️ Weather Agent LangGraph</strong><br>
  <em>AI-powered weather intelligence at your fingertips</em><br>
  <sub>Built with ❤️ by <a href="https://github.com/CodexJitin">CodexJitin</a></sub>
</p>