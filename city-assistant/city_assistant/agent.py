from google.adk.agents import Agent

from .prompt import agent_instruction
from .tools.tools import get_weather, get_current_time

root_agent = Agent(
    model="gemini-2.5-flash",
    name="city_assistant",
    instruction=agent_instruction,
    tools=[get_weather, get_current_time],
)