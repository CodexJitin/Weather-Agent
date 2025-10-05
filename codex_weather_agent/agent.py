"""
Weather Agent with configurable LLM support and memory management.
"""

import json
from typing import Dict, List, Any, Literal, Union, Optional
from typing_extensions import TypedDict, Annotated

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseChatModel
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from .config import LLMConfig, WeatherConfig, CONVERSATIONAL_SYSTEM_PROMPT
from .exceptions import WeatherAgentError, LLMConfigError, APIKeyError
from .llm_factory import create_llm
from .tools import get_weather_tools


class WeatherAgentState(TypedDict):
    """State definition for the weather agent."""
    messages: Annotated[List[BaseMessage], add_messages]


class WeatherAgent:
    """
    LangGraph Weather Agent with configurable LLM support and memory management.
    
    Features:
    - Configurable LLM providers (Google, OpenAI, Anthropic)
    - Conversation memory management
    - Natural conversational responses
    - Comprehensive weather tools
    - Error handling and recovery
    """
    
    def __init__(
        self, 
        llm_config: Optional[LLMConfig] = None,
        weather_config: Optional[WeatherConfig] = None,
        max_memory_conversations: int = 5,
        custom_llm: Optional[BaseChatModel] = None
    ):
        """
        Initialize the weather agent.
        
        Args:
            llm_config: Configuration for LLM provider
            weather_config: Configuration for weather services
            max_memory_conversations: Maximum conversations to keep in memory
            custom_llm: Custom LLM instance (overrides llm_config)
        """
        # Set default configurations
        self.llm_config = llm_config or LLMConfig()
        self.weather_config = weather_config or WeatherConfig()
        self.max_memory_conversations = max_memory_conversations
        
        # Initialize LLM
        if custom_llm:
            self.llm = custom_llm
        else:
            self.llm = create_llm(self.llm_config)
        
        # Get weather tools with configuration
        self.weather_tools = get_weather_tools(self.weather_config)
        
        # Bind tools to LLM
        self.llm_with_tools = self.llm.bind_tools(self.weather_tools)
        
        # Create tool node for executing tools
        self.tool_node = ToolNode(self.weather_tools)
        
        # Memory management
        self.conversation_memory: List[BaseMessage] = []
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph state graph."""
        workflow = StateGraph(WeatherAgentState)
        
        # Add nodes
        workflow.add_node("agent", self._agent_node)
        workflow.add_node("tools", self.tool_node)
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add conditional edges
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END,
            },
        )
        
        # Add edge from tools back to agent
        workflow.add_edge("tools", "agent")
        
        return workflow.compile()
    
    def _manage_memory(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """
        Manage conversation memory to keep only the last N conversations.
        
        Args:
            messages: Current message list
            
        Returns:
            Trimmed message list with system prompt + last N conversations
        """
        # Always keep system prompt (first message if it's a HumanMessage with system content)
        system_messages = []
        conversation_messages = []
        
        for msg in messages:
            if (isinstance(msg, HumanMessage) and 
                CONVERSATIONAL_SYSTEM_PROMPT in getattr(msg, 'content', '')):
                system_messages.append(msg)
            else:
                conversation_messages.append(msg)
        
        # Count conversations (pairs of Human + AI messages, plus any tool messages)
        conversation_count = 0
        kept_messages = []
        temp_conversation = []
        
        # Process messages in reverse to keep the most recent conversations
        for msg in reversed(conversation_messages):
            temp_conversation.insert(0, msg)
            
            # Count a conversation when we see a HumanMessage (start of conversation)
            if isinstance(msg, HumanMessage) and not any(CONVERSATIONAL_SYSTEM_PROMPT in getattr(m, 'content', '') for m in [msg]):
                conversation_count += 1
                if conversation_count <= self.max_memory_conversations:
                    kept_messages = temp_conversation + kept_messages
                    temp_conversation = []
                else:
                    break
        
        # Combine system messages + kept conversations
        return system_messages + kept_messages
    
    def _agent_node(self, state: WeatherAgentState) -> Dict[str, List[BaseMessage]]:
        """
        Main agent node that processes messages and decides on tool usage.
        
        Args:
            state: Current agent state with message history
            
        Returns:
            Updated state with new messages
        """
        messages = state["messages"]
        
        # Add system prompt if this is the first interaction
        if not any(isinstance(msg, AIMessage) for msg in messages):
            # Insert system prompt as the first message (convert to human for Gemini)
            system_message = HumanMessage(content=CONVERSATIONAL_SYSTEM_PROMPT)
            messages = [system_message] + messages
        
        # Apply memory management to keep only last N conversations
        messages = self._manage_memory(messages)
        
        # Get response from LLM
        response = self.llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    def _should_continue(self, state: WeatherAgentState) -> Literal["continue", "end"]:
        """
        Determine whether to continue with tool execution or end.
        
        Args:
            state: Current agent state
            
        Returns:
            "continue" if tools should be executed, "end" if conversation should end
        """
        messages = state["messages"]
        last_message = messages[-1]
        
        # If the last message has tool calls, continue to tools
        if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"
        
        # Otherwise, end the conversation
        return "end"
    
    def chat(self, message: str) -> str:
        """
        Send a message to the weather agent and get a response.
        
        Args:
            message: User message/question about weather
            
        Returns:
            Agent's response as a string
            
        Raises:
            WeatherAgentError: If there's an error processing the message
        """
        try:
            # Create initial state
            initial_state: WeatherAgentState = {
                "messages": [HumanMessage(content=message)]
            }
            
            # Run the graph
            result = self.graph.invoke(initial_state)
            
            # Extract the final response
            final_message = result["messages"][-1]
            if isinstance(final_message, AIMessage):
                content = final_message.content
                return content if isinstance(content, str) else str(content)
            else:
                return str(final_message.content)
                
        except Exception as e:
            raise WeatherAgentError(f"Error processing message: {str(e)}") from e
    
    def stream_chat(self, message: str):
        """
        Stream chat interface for real-time responses.
        
        Args:
            message: User message/question about weather
            
        Yields:
            Streaming response chunks
            
        Raises:
            WeatherAgentError: If there's an error during streaming
        """
        try:
            initial_state: WeatherAgentState = {
                "messages": [HumanMessage(content=message)]
            }
            
            for chunk in self.graph.stream(initial_state):
                if "agent" in chunk:
                    if chunk["agent"]["messages"]:
                        msg = chunk["agent"]["messages"][-1]
                        if isinstance(msg, AIMessage) and msg.content:
                            yield msg.content
                            
        except Exception as e:
            raise WeatherAgentError(f"Error during streaming: {str(e)}") from e
    
    def clear_memory(self):
        """Clear the conversation memory."""
        self.conversation_memory = []
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get information about current memory usage."""
        conversation_count = sum(1 for msg in self.conversation_memory 
                               if isinstance(msg, HumanMessage) and 
                               CONVERSATIONAL_SYSTEM_PROMPT not in getattr(msg, 'content', ''))
        
        return {
            "max_conversations": self.max_memory_conversations,
            "current_conversations": conversation_count,
            "total_messages": len(self.conversation_memory),
            "llm_provider": self.llm_config.provider,
            "llm_model": self.llm_config.model
        }
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return [tool.name for tool in self.weather_tools]
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """Get descriptions of all available tools."""
        return {tool.name: tool.description for tool in self.weather_tools}


def create_weather_agent(
    llm_provider: Literal["google", "openai", "anthropic", "custom"],
    llm_model: str,
    llm_api_key: str,
    openweather_api_key: str,
    max_memory_conversations: int = 5,
    llm_temperature: float = 0.1,
    custom_llm: Optional[BaseChatModel] = None,
    **llm_kwargs
) -> WeatherAgent:
    """
    Factory function to create a configured weather agent.
    
    Args:
        llm_provider: LLM provider ("google", "openai", "anthropic", "custom") - REQUIRED
        llm_model: Model name for the provider - REQUIRED
        llm_api_key: API key for the LLM provider - REQUIRED
        openweather_api_key: OpenWeather API key - REQUIRED
        max_memory_conversations: Maximum conversations to keep in memory (default: 5)
        llm_temperature: Temperature for LLM responses (default: 0.1)
        custom_llm: Custom LLM instance (overrides other LLM settings)
        **llm_kwargs: Additional LLM parameters
    
    Returns:
        WeatherAgent: Ready-to-use weather agent instance
        
    Raises:
        LLMConfigError: If LLM configuration is invalid
        APIKeyError: If required API keys are missing
        WeatherAgentError: If agent creation fails
        
    Example:
        >>> agent = create_weather_agent(
        ...     llm_provider="google",
        ...     llm_model="gemini-2.5-flash", 
        ...     llm_api_key="your-google-api-key",
        ...     openweather_api_key="your-openweather-key"
        ... )
    """
    try:
        # Create configurations
        llm_config = LLMConfig(
            provider=llm_provider,
            model=llm_model,
            api_key=llm_api_key,
            temperature=llm_temperature,
            additional_params=llm_kwargs
        )
        
        weather_config = WeatherConfig(
            openweather_api_key=openweather_api_key
        )
        
        # Create agent
        agent = WeatherAgent(
            llm_config=llm_config,
            weather_config=weather_config,
            max_memory_conversations=max_memory_conversations,
            custom_llm=custom_llm
        )
        
        return agent
        
    except Exception as e:
        if isinstance(e, (LLMConfigError, APIKeyError)):
            raise
        else:
            raise WeatherAgentError(f"Failed to create weather agent: {str(e)}") from e