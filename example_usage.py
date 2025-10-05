"""
Simple usage example for Codex Weather Agent

NOTE: Starting from version 1.0.4, ALL API keys are REQUIRED!
You must provide both LLM API key and OpenWeather API key.
"""

from codex_weather_agent import create_weather_agent

def main():
    """Example of using the weather agent with different LLM providers"""
    
    # ⚠️ IMPORTANT: ALL PARAMETERS ARE REQUIRED ⚠️
    # You must provide:
    # 1. llm_provider (google/openai/anthropic)
    # 2. llm_model (specific model name)
    # 3. llm_api_key (your LLM provider API key)
    # 4. openweather_api_key (your OpenWeather API key)
    
    print("🌤️ Codex Weather Agent v1.0.4 - Example Usage")
    print("Author: CodexJitin")
    print("=" * 50)
    
    # Example 1: Using Google Gemini (REQUIRED PARAMETERS)
    print("Creating weather agent with Google Gemini...")
    print("⚠️  All API keys are now MANDATORY!")
    
    try:
        agent = create_weather_agent(
            llm_provider="google",                    # REQUIRED
            llm_model="gemini-2.5-flash",            # REQUIRED  
            llm_api_key="your-google-api-key-here",  # REQUIRED - Replace with real key!
            openweather_api_key="your-weather-key-here"  # REQUIRED - Replace with real key!
            # Set via environment variables instead:
            # export GOOGLE_API_KEY="your-key-here"
            # export OPENWEATHER_API_KEY="your-key-here"
        )
        
        # Natural conversation
        print("\n--- Natural Weather Conversation ---")
        response = agent.chat("What's the weather like right now?")
        print(f"Agent: {response}")
        
        response = agent.chat("How about tomorrow?")
        print(f"Agent: {response}")
        
        # Check memory
        memory_info = agent.get_memory_info()
        print(f"\nMemory: {memory_info['current_conversations']} conversations")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure to:")
        print("   1. Replace 'your-google-api-key-here' with your actual Google API key")
        print("   2. Replace 'your-weather-key-here' with your actual OpenWeather API key")
        print("   3. Or set environment variables: GOOGLE_API_KEY and OPENWEATHER_API_KEY")
        return
    
    # Example 2: Using OpenAI (commented out - requires valid keys)
    """
    print("\n--- Using OpenAI ---")
    openai_agent = create_weather_agent(
        llm_provider="openai",                      # REQUIRED
        llm_model="gpt-4",                         # REQUIRED
        llm_api_key="your-openai-key-here",       # REQUIRED
        openweather_api_key="your-weather-key-here"  # REQUIRED
    )
    
    response = openai_agent.chat("What's the air quality in Tokyo?")
    print(f"OpenAI Agent: {response}")
    """
    
    # Example 3: Streaming responses
    print("\n--- Streaming Response ---")
    print("Agent: ", end="", flush=True)
    for chunk in agent.stream_chat("Tell me about the weather in Paris"):
        print(chunk, end="", flush=True)
    print()  # New line after streaming
    
    # Clear memory
    agent.clear_memory()
    print(f"\nMemory cleared. Conversations: {agent.get_memory_info()['current_conversations']}")

if __name__ == "__main__":
    main()