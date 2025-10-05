# Codex Weather Agent 🌤️

A conversational weather agent powered by LangGraph with configurable LLM support and intelligent conversation memory.

[![PyPI version](https://badge.fury.io/py/codex-weather-agent.svg)](https://badge.fury.io/py/codex-weather-agent)
[![Version](https://img.shields.io/badge/version-1.0.5-blue.svg)](https://github.com/CodexJitin/codex-weather-agent)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Author](https://img.shields.io/badge/author-CodexJitin-orange.svg)](https://github.com/CodexJitin)

## 🚀 Features

### 🤖 Configurable LLM Support

- **Google Gemini** (2.5 Flash, 2.5 Pro, 2.0 Flash)
- **OpenAI** (GPT-4, GPT-4 Turbo, GPT-3.5 Turbo) 
- **Anthropic Claude** (Claude 3 Sonnet, Haiku, Claude 2)
- **Custom LLM** support for any LangChain-compatible model

### 🌍 Comprehensive Weather Data
- **Current Weather** - Real-time conditions for any city
- **5-Day Forecasts** - Detailed predictions with 3-hour intervals
- **Air Quality** - Pollution levels and air quality indices
- **Location Detection** - Automatic IP-based location discovery
- **Geocoding** - Convert location names to coordinates

### 💬 Natural Conversation
- **Memory Management** - Remembers conversation context (configurable)
- **Conversational Style** - Natural responses without bullet points or lists
- **Streaming Support** - Real-time response generation
- **Error Recovery** - Graceful handling of API failures

## 📦 Installation

### Basic Installation

```bash
pip install codex-weather-agent
```

### With specific LLM providers

```bash
# For Google Gemini (recommended)
pip install codex-weather-agent[google]

# For OpenAI 
pip install codex-weather-agent[openai]

# For Anthropic Claude
pip install codex-weather-agent[anthropic]

# For all providers
pip install codex-weather-agent[all]
```

## 🔧 Quick Start

### Basic Usage with Google Gemini

```python
from codex_weather_agent import create_weather_agent

# Create agent with Google Gemini (ALL PARAMETERS REQUIRED)
agent = create_weather_agent(
    llm_provider="google",                    # REQUIRED: Choose your LLM provider
    llm_model="gemini-2.5-flash",            # REQUIRED: Specify model name
    llm_api_key="your-google-api-key",       # REQUIRED: Your LLM API key
    openweather_api_key="your-openweather-key"  # REQUIRED: OpenWeather API key
)

# Have a natural conversation about weather
response = agent.chat("What's the weather like right now?")
print(response)

response = agent.chat("How about tomorrow in Tokyo?")
print(response)
```

### Using Different LLM Providers

```python
# OpenAI GPT-4 (ALL PARAMETERS REQUIRED)
agent = create_weather_agent(
    llm_provider="openai",
    llm_model="gpt-4",
    llm_api_key="your-openai-key",           # REQUIRED
    openweather_api_key="your-weather-key"   # REQUIRED
)

# Anthropic Claude (ALL PARAMETERS REQUIRED)
agent = create_weather_agent(
    llm_provider="anthropic", 
    llm_model="claude-3-sonnet",
    llm_api_key="your-anthropic-key",        # REQUIRED
    openweather_api_key="your-weather-key"   # REQUIRED
)

# Custom LLM
from langchain_openai import ChatOpenAI
custom_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

agent = create_weather_agent(
    llm_provider="custom",
    llm_model="custom",  # Can be any string for custom LLM
    llm_api_key="not-used-for-custom",       # Still required
    openweather_api_key="your-weather-key",  # REQUIRED
    custom_llm=custom_llm
)
```

### Advanced Configuration

```python
from codex_weather_agent import WeatherAgent, LLMConfig, WeatherConfig

# Detailed configuration
llm_config = LLMConfig(
    provider="google",
    model="gemini-2.5-flash",
    temperature=0.1,
    max_tokens=1000,
    api_key="your-api-key"
)

weather_config = WeatherConfig(
    openweather_api_key="your-weather-key",
    request_timeout=10,
    default_units="metric"
)

# Create agent with custom configurations
agent = WeatherAgent(
    llm_config=llm_config,
    weather_config=weather_config,
    max_memory_conversations=10  # Remember last 10 conversations
)
```

### Streaming Responses

```python
# Get real-time streaming responses
for chunk in agent.stream_chat("Tell me about the weather in Paris"):
    print(chunk, end="", flush=True)
```

### Memory Management

```python
# Check memory usage
memory_info = agent.get_memory_info()
print(f"Conversations in memory: {memory_info['current_conversations']}")
print(f"LLM Provider: {memory_info['llm_provider']}")

# Clear conversation memory
agent.clear_memory()
```

## 🔑 API Keys (REQUIRED)

### ⚠️ **All API Keys Are Now Mandatory**

Starting from version 1.0.4, **ALL API keys are required** for the weather agent to function. This ensures reliable operation and prevents rate limiting issues.

### Required API Keys

1. **LLM Provider API Key** (mandatory - choose one):
   - **Google**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - **OpenAI**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
   - **Anthropic**: Get from [Anthropic Console](https://console.anthropic.com/)

2. **OpenWeather API Key** (mandatory):
   - Get from [OpenWeatherMap](https://openweathermap.org/api)
   - Free tier available with 1,000 calls/day
   - **No longer optional** - you must provide your own key

### Setting API Keys

#### Environment Variables (Recommended)
```bash
export GOOGLE_API_KEY="your-google-api-key"
export OPENWEATHER_API_KEY="your-openweather-key"
```

#### Direct Parameter Passing
```python
agent = create_weather_agent(
    llm_api_key="your-llm-api-key",
    openweather_api_key="your-weather-key"
)
```

## 🌟 Example Conversations

The agent responds naturally without structured formatting:

```python
agent = create_weather_agent(
    llm_provider="google", 
    llm_model="gemini-2.5-flash",
    llm_api_key="your-key",
    openweather_api_key="your-weather-key"
)

# Natural weather queries
print(agent.chat("Hey, what's it like outside?"))
# "Hey there! Let me check your current location... It looks like you're in New York, and it's a beautiful sunny day with 72°F and clear skies!"

print(agent.chat("Should I bring an umbrella tomorrow?"))  
# "Based on tomorrow's forecast for New York, you should definitely grab an umbrella! There's rain expected in the afternoon with about 80% chance of precipitation..."

print(agent.chat("What about the air quality?"))
# "The air quality in your area is pretty good today with an AQI of 45, which means it's safe for outdoor activities and everyone can enjoy being outside!"
```

## 🛠️ Available Tools

The agent has access to these weather tools:

- `current_location()` - Detect user's location via IP
- `get_current_weather(city)` - Current weather conditions
- `get_weather_forecast(city)` - 5-day weather forecast
- `get_air_pollution(lat, lon)` - Air quality data
- `get_location_coordinates(location)` - Geocoding service

## 🔧 Configuration Options

### LLM Configuration

```python
from codex_weather_agent import LLMConfig

config = LLMConfig(
    provider="google",  # "google", "openai", "anthropic", "custom"
    model="gemini-2.5-flash",
    api_key="your-key",
    temperature=0.1,    # Response randomness (0.0-1.0)
    max_tokens=1000,    # Maximum response length
    top_p=0.8,         # Nucleus sampling (Google only)
    top_k=40,          # Top-k sampling (Google only)
    additional_params={}  # Provider-specific parameters
)
```

#### Supported Models by Provider

| Provider | Supported Models |
|----------|------------------|
| **Google Gemini** | `gemini-2.5-flash`, `gemini-2.5-pro`, `gemini-2.0-flash` |
| **OpenAI** | `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` |
| **Anthropic** | `claude-3-sonnet`, `claude-3-haiku`, `claude-2` |
| **Custom** | Any model supported by your custom LLM instance |

### Weather Configuration  

```python
from codex_weather_agent import WeatherConfig

config = WeatherConfig(
    openweather_api_key="your-key",
    request_timeout=5,           # API request timeout
    max_retries=3,              # Number of retry attempts
    enable_location_detection=True,  # Auto-detect user location
    default_units="metric"       # "metric", "imperial", "kelvin"
)
```

## 🧪 Error Handling

The package includes comprehensive error handling:

```python
from codex_weather_agent import WeatherAgentError, LLMConfigError, APIKeyError

try:
    agent = create_weather_agent(llm_provider="invalid")
except LLMConfigError as e:
    print(f"LLM configuration error: {e}")

try:
    response = agent.chat("What's the weather?")
except WeatherAgentError as e:
    print(f"Weather agent error: {e}")
```

## 📋 Requirements

- Python 3.8+
- Internet connection for weather data and LLM APIs
- Valid API keys for your chosen LLM provider

### Core Dependencies
- `requests>=2.31.0`
- `langchain-core>=0.3.0`
- `langgraph>=0.2.0`
- `typing-extensions>=4.7.0`

### Optional Dependencies
- `langchain-google-genai>=2.0.0` (for Google Gemini)
- `langchain-openai>=0.2.0` (for OpenAI models)
- `langchain-anthropic>=0.2.0` (for Anthropic Claude)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **PyPI**: <https://pypi.org/project/codex-weather-agent/>
- **GitHub**: <https://github.com/CodexJitin/codex-weather-agent>
- **Documentation**: <https://github.com/CodexJitin/codex-weather-agent#readme>
- **Issues**: <https://github.com/CodexJitin/codex-weather-agent/issues>

---

Made with ❤️ by CodexJitin