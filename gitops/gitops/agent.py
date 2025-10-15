from google.adk.agents import Agent

from .prompt import agent_instruction
# from .tools.tools import argocd_tools, github_tools
from .tools.tools import github_tools

root_agent = Agent(
    model="gemini-2.5-flash",
    name="gitops",
    instruction=agent_instruction,
    # tools=[argocd_tools, github_tools],
    tools=[github_tools],    
)