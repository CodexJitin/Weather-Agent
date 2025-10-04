"""LangGraph workflow implementation for the weather agent with optimized performance."""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import functools

from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import BaseTool

from .state import WeatherAgentState
from .tools import get_weather, get_air_pollution, current_location, get_forecast, get_location_coordinates
from .llm_providers.base import LLMProvider


class WeatherAgentWorkflow:
    """LangGraph workflow for weather assistant with performance optimizations."""
    
    def __init__(self, llm_provider: LLMProvider, openweather_api_key: str = None):
        """Initialize the weather agent workflow.
        
        Args:
            llm_provider: LLM provider instance
            openweather_api_key: OpenWeatherMap API key (optional, uses environment variable if not provided)
        """
        self.llm = llm_provider.llm
        self.openweather_api_key = openweather_api_key
        
        # Pre-create tool map for faster lookup (O(1) instead of O(n))
        self.tools = [
            get_weather,
            get_air_pollution,
            current_location,
            get_forecast,
            get_location_coordinates,
        ]
        self.tool_map = {tool.name: tool for tool in self.tools}
        
        # Cache system prompt for reuse
        self._system_prompt = self._build_system_prompt()
        self.graph = self._build_graph()
    
    def _build_system_prompt(self) -> str:
        """Build and cache the system prompt to avoid rebuilding on each request."""
        current_datetime = datetime.now().strftime("%A, %d %B %Y %I:%M %p")
        return f"""
System: You are a weather information assistant developed by CodexJitin. 
Current date and time: {current_datetime}

Your job is to talk naturally with the user while giving accurate weather updates. 
Keep your tone conversational, like you're chatting with someone, but always base your answers on the tools you have.

Guidelines:
- Speak clearly and directly, avoid lists or bullet points.
- When someone asks about air quality, first grab the location coordinates, then check the air quality.
- If the user does not mention a city name, use their current location instead.
- Stay focused only on weather and details about yourself as the assistant.
- If the user brings up anything outside of weather, reply with: "I can only assist with weather-related queries."
"""
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(WeatherAgentState)
        
        # Add nodes
        workflow.add_node("initialize", self._initialize_node)
        workflow.add_node("analyze_query", self._analyze_query_node)
        workflow.add_node("execute_tools", self._execute_tools_node)
        workflow.add_node("generate_response", self._generate_response_node)
        workflow.add_node("finalize", self._finalize_node)
        
        # Add edges
        workflow.set_entry_point("initialize")
        workflow.add_edge("initialize", "analyze_query")
        workflow.add_edge("analyze_query", "execute_tools")
        workflow.add_edge("execute_tools", "generate_response")
        workflow.add_edge("generate_response", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    @functools.lru_cache(maxsize=1)
    def _get_system_prompt_template(self) -> str:
        """Get cached system prompt template."""
        return """
You are a weather information assistant developed by CodexJitin. 
Current date and time: {current_datetime}

Your job is to talk naturally with the user while giving accurate weather updates. 
Keep your tone conversational, like you're chatting with someone, but always base your answers on the tools you have.

Guidelines:
- Speak clearly and directly, avoid lists or bullet points.
- When someone asks about air quality, first grab the location coordinates, then check the air quality.
- If the user does not mention a city name, use their current location instead.
- Stay focused only on weather and details about yourself as the assistant.
- If the user brings up anything outside of weather, reply with: "I can only assist with weather-related queries."

Available tools:
- get_weather: Get current weather for a city
- get_forecast: Get 5-day weather forecast for a city
- get_air_pollution: Get air quality data (requires coordinates)
- get_location_coordinates: Get coordinates for a location name
- current_location: Get user's current location based on IP

Use these tools as needed to provide accurate weather information.
"""

    def _initialize_node(self, state: WeatherAgentState) -> WeatherAgentState:
        """Initialize the workflow state."""
        current_datetime = datetime.now().strftime("%A, %d %B %Y %I:%M %p")
        system_prompt = self._get_system_prompt_template().format(current_datetime=current_datetime)
        
        state["messages"] = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=state["query"])
        ]
        state["tool_calls"] = []
        state["tool_results"] = []
        state["is_complete"] = False
        state["error"] = None
        
        return state
    
    def _analyze_query_node(self, state: WeatherAgentState) -> WeatherAgentState:
        """Analyze the user query and determine what tools to use."""
        try:
            # Bind tools to the LLM
            llm_with_tools = self.llm.bind_tools(self.tools)
            
            # Get LLM response with tool calls
            response = llm_with_tools.invoke(state["messages"])
            state["messages"].append(response)
            
            # Extract tool calls if any
            if hasattr(response, 'tool_calls') and response.tool_calls:
                state["tool_calls"] = response.tool_calls
            else:
                # No tools needed, just generate response
                state["next_action"] = "generate_response"
                
        except Exception as e:
            state["error"] = f"Error analyzing query: {str(e)}"
            state["next_action"] = "finalize"
            
        return state
    
    @functools.lru_cache(maxsize=100)
    def _cached_tool_execution(self, tool_name: str, tool_args_str: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Cache tool results to avoid redundant API calls."""
        tool = self.tool_map.get(tool_name)
        if not tool:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            # Parse args back from string
            tool_args = json.loads(tool_args_str)
            
            # Add API key for OpenWeatherMap tools
            if tool_name in ["get_weather", "get_air_pollution", "get_forecast", "get_location_coordinates"] and api_key:
                tool_args["api_key"] = api_key
            
            return tool.invoke(tool_args)
        except Exception as e:
            return {"error": f"Error executing tool {tool_name}: {str(e)}"}

    def _execute_tools_node(self, state: WeatherAgentState) -> WeatherAgentState:
        """Execute the requested tools with caching."""
        if not state["tool_calls"]:
            return state
            
        tool_results = []
        
        for tool_call in state["tool_calls"]:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            # Use cached execution for better performance
            tool_args_str = json.dumps(tool_args, sort_keys=True)
            result = self._cached_tool_execution(
                tool_name, 
                tool_args_str, 
                self.openweather_api_key
            )
            
            if "error" not in result:
                # Store results in state for potential reuse
                if tool_name == "current_location":
                    state["current_location"] = result
                elif tool_name == "get_location_coordinates":
                    state["coordinates"] = result
                elif tool_name == "get_weather":
                    state["weather_data"] = result
                elif tool_name == "get_forecast":
                    state["forecast_data"] = result
                elif tool_name == "get_air_pollution":
                    state["pollution_data"] = result
                
                tool_results.append({
                    "tool_call_id": tool_call["id"],
                    "tool_name": tool_name,
                    "result": result
                })
                
                # Add tool message to conversation
                state["messages"].append(
                    ToolMessage(
                        content=json.dumps(result),
                        tool_call_id=tool_call["id"]
                    )
                )
            else:
                tool_results.append({
                    "tool_call_id": tool_call["id"],
                    "tool_name": tool_name,
                    "error": result["error"]
                })
        
        state["tool_results"] = tool_results
        return state
    
    def _generate_response_node(self, state: WeatherAgentState) -> WeatherAgentState:
        """Generate the final response based on tool results."""
        try:
            # Get final response from LLM
            response = self.llm.invoke(state["messages"])
            state["response"] = response.content
            state["messages"].append(response)
            
        except Exception as e:
            state["error"] = f"Error generating response: {str(e)}"
            state["response"] = "I apologize, but I encountered an error while processing your request."
            
        return state
    
    def _finalize_node(self, state: WeatherAgentState) -> WeatherAgentState:
        """Finalize the workflow."""
        state["is_complete"] = True
        
        # If there's an error and no response, provide a default error message
        if state["error"] and not state["response"]:
            state["response"] = "I apologize, but I encountered an error while processing your weather request. Please try again."
            
        return state
    
    def process_query(self, query: str) -> str:
        """Process a weather query and return the response.
        
        Args:
            query: User's weather query
            
        Returns:
            Weather assistant's response
        """
        initial_state: WeatherAgentState = {
            "query": query,
            "response": None,
            "messages": [],
            "tool_calls": [],
            "tool_results": [],
            "current_location": None,
            "target_location": None,
            "coordinates": None,
            "weather_data": None,
            "forecast_data": None,
            "pollution_data": None,
            "next_action": None,
            "error": None,
            "is_complete": False,
        }
        
        try:
            final_state = self.graph.invoke(initial_state)
            return final_state.get("response", "I couldn't process your request. Please try again.")
        except Exception as e:
            return f"An error occurred: {str(e)}"