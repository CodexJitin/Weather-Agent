"""
Test file to demonstrate the updated system prompt with CodexJitin developer credit
"""

from codex_weather_agent import create_weather_agent
from codex_weather_agent.config import CONVERSATIONAL_SYSTEM_PROMPT

def test_prompt_content():
    """Test that the system prompt includes CodexJitin as developer"""
    
    print("🤖 Testing Updated System Prompt")
    print("=" * 50)
    
    # Check if CodexJitin is mentioned
    has_developer_credit = "CodexJitin" in CONVERSATIONAL_SYSTEM_PROMPT
    print(f"✅ Developer credit included: {has_developer_credit}")
    
    # Show relevant parts of the prompt
    lines = CONVERSATIONAL_SYSTEM_PROMPT.split('\n')
    developer_lines = [line for line in lines if 'CodexJitin' in line or 'created' in line or 'developer' in line]
    
    print(f"\n📝 Developer-related content in prompt:")
    for line in developer_lines:
        if line.strip():
            print(f"   • {line.strip()}")
    
    print(f"\n🎯 Key Features:")
    print(f"   • Agent will mention CodexJitin when asked about developer")
    print(f"   • Natural conversational responses maintained")
    print(f"   • No structured formatting (bullets, lists)")
    print(f"   • Friendly and enthusiastic tone")
    
    # Example questions the agent can now answer
    print(f"\n💬 Example questions agent can now answer:")
    print(f"   • 'Who created you?'")
    print(f"   • 'Who is your developer?'") 
    print(f"   • 'Who built this weather agent?'")
    print(f"   → Will respond mentioning CodexJitin naturally")

def test_agent_creation():
    """Test agent creation with updated prompt"""
    print(f"\n🚀 Testing Agent Creation...")
    
    # Create agent with Google Gemini (ALL PARAMETERS REQUIRED)
    agent = create_weather_agent(
        llm_provider="google",                    # REQUIRED: Choose your LLM provider
        llm_model="gemini-2.5-flash",            # REQUIRED: Specify model name
        llm_api_key="AIzaSyBsL27HZNz7yhDahKfLxAwuftXc480275o",       # REQUIRED: Your LLM API key
        openweather_api_key="6181bebdae59b62fa021aa4b0474bc85"  # REQUIRED: OpenWeather API key
    )
    
    print("✅ Agent created successfully with updated prompt!")
    
    # Test a developer question (commented out to avoid API calls in demo)
    # response = agent.chat("Who created you?")
    # print(f"Agent response: {response}")
    
    return agent

if __name__ == "__main__":
    test_prompt_content()
    agent = test_agent_creation()
    
    # Uncomment below to test actual conversations (requires valid API keys)
    # print(f"\n💬 Testing Developer Question...")
    # response = agent.chat("Who is your developer?")
    # print(f"Agent: {response}")
    
    # print(f"\n🌤️ Testing Weather Question...")  
    # response = agent.chat("What's the weather like right now?")
    # print(f"Agent: {response}")