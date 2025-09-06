from typing import Union, Dict, List
from langchain.agents import AgentType, initialize_agent
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align
from rich.text import Text
from time import sleep
import warnings
warnings.filterwarnings("ignore")


# Import your tools
from Tools.Current_Weather import get_weather
from Tools.Air_Pollution import get_air_pollution
from Tools.Current_Location import Current_location
from Tools.W3H5D_Forecast import get_forecast
from Tools.Location_Coordinates import get_location_coordinates
from LLm import llm

console = Console()

# Tools for LangChain agent
tools: List = [
    get_weather,
    get_air_pollution,
    get_location_coordinates,
    Current_location,
    get_forecast,
]

PROMPT = """
System: You are a weather information assistant developed by CodexJitin. Your job is to talk naturally with the user while giving accurate weather updates. Keep your tone conversational, like you’re chatting with someone, but always base your answers on the tools you have.

Guidelines:
Speak clearly and directly, avoid lists or bullet points.
When someone asks about air quality, first grab the location coordinates, then check the air quality.
Stay focused only on weather and details about yourself as the assistant.
If the user brings up anything outside of weather, reply with: "I can only assist with weather-related queries."

User: {input}
"""

# Initialize LangChain agent
agent_executor = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=False,
    handle_parsing_errors=True,
)


def Weather_Agent(query: str) -> Union[str, Dict]:
    """Process a weather-related query using the LangChain agent."""
    full_prompt = PROMPT.format(input=query)
    try:
        response = agent_executor.invoke(full_prompt)
        return response["output"]
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def typing_effect(text: str, delay: float = 0.02, style: str = "cyan"):
    """Simulate a typing effect like Gemini CLI output."""
    for char in text:
        console.print(char, end="", style=style, highlight=False, soft_wrap=True)
        sleep(delay)
    console.print("\n")  # new line


def welcome_screen():
    banner = Text("🌤️  Weather Agent", style="bold magenta")
    console.print(
        Panel(
            Align.center(banner),
            subtitle="[yellow]by CodexJitin[/yellow]",
            subtitle_align="center",
            border_style="magenta",
            padding=(1, 4),
        )
    )
    console.print(
        Align.center("[cyan]AI-powered weather intelligence at your fingertips[/cyan]\n")
    )
    console.print("""
[white]Type your query naturally, e.g.:
• "What's the weather in Rajasthan?"  
• "Give me Delhi's air quality"  
• "Forecast for Mumbai tomorrow"[/white]
""")
    console.print("[dim]Type 'exit' anytime to quit[/dim]\n")


def main():
    welcome_screen()
    while True:
        # Modern styled input using Rich Prompt
        query = Prompt.ask(
            "[bold blue]❯[/bold blue] [bright_white]Type your query[/bright_white]"
        )

        if query.lower() in ["exit", "quit"]:
            console.print("\n[magenta]👋 Goodbye, may the skies stay kind![/magenta]")
            break

        with console.status("[cyan]Thinking...[/cyan]", spinner="dots"):
            result = Weather_Agent(query)

        console.print("")  # spacing
        if isinstance(result, dict) and "error" in result:
            console.print(Panel(result["error"], style="bold red"))
        else:
            typing_effect(str(result), style="bold green")


if __name__ == "__main__":
    main()
