"""Base agent class with memory integration for all specialized agents."""
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.memori import MemoriTools
from typing import List, Optional
from config.settings import (
    DEFAULT_MODEL,
    MODEL_TEMPERATURE,
    AGENT_CONFIG,
    GOOGLE_API_KEY
)
from memory.memory_manager import get_memory_tools_for_context


class BaseAgent:
    """Base class for all Effectiva agents with memory integration."""
    
    def __init__(
        self,
        name: str,
        role: str,
        context: str,
        instructions: str,
        tools: Optional[List] = None,
        add_memory: bool = True
    ):
        """
        Initialize a base agent with memory capabilities.
        
        Args:
            name: Agent name
            role: Agent role/description
            context: Memory context (study, work, life, scheduling, coordinator)
            instructions: Agent instructions/persona
            tools: List of tools the agent can use
            add_memory: Whether to add memory tools
        """
        self.name = name
        self.role = role
        self.context = context
        
        # Initialize tools list
        agent_tools = tools or []
        
        # Add memory tools if requested
        if add_memory:
            memory_tools = get_memory_tools_for_context(context)
            agent_tools.append(memory_tools)
        
        # Create the agent
        self.agent = Agent(
            name=name,
            role=role,
            model=Gemini(id=DEFAULT_MODEL, api_key=GOOGLE_API_KEY),
            tools=agent_tools,
            instructions=instructions,
            markdown=AGENT_CONFIG["markdown"],
            show_tool_calls=AGENT_CONFIG["show_tool_calls"],
            temperature=MODEL_TEMPERATURE
        )
    
    def run(self, message: str, **kwargs):
        """
        Run the agent with a message.
        
        Args:
            message: User message
            **kwargs: Additional arguments to pass to agent
            
        Returns:
            Agent response
        """
        return self.agent.run(message, **kwargs)
    
    def get_agent(self) -> Agent:
        """
        Get the underlying Agno agent.
        
        Returns:
            Agno Agent instance
        """
        return self.agent
