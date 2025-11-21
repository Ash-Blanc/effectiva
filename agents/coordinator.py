"""Coordinator agent that orchestrates the multi-agent team."""
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from typing import Optional
from textwrap import dedent

from agents.study_agent import create_study_agent
from agents.work_agent import create_work_agent
from agents.life_agent import create_life_agent
from agents.scheduling_agent import create_scheduling_agent
from tools.context_tools import (
    switch_context, get_current_context,
    get_context_suggestions, view_context_history
)
from config.settings import (
    DEFAULT_MODEL,
    MODEL_TEMPERATURE,
    AGENT_CONFIG,
    GOOGLE_API_KEY
)
from memory.memory_manager import get_memory_tools_for_context


def create_coordinator_agent() -> Team:
    """
    Create the Coordinator Agent that manages the multi-agent team.
    
    Returns:
        Agno Team instance configured as coordinator
    """
    # Create specialist agents
    study_agent = create_study_agent().get_agent()
    work_agent = create_work_agent().get_agent()
    life_agent = create_life_agent().get_agent()
    scheduling_agent = create_scheduling_agent().get_agent()
    
    # Coordinator instructions
    coordinator_instructions = dedent("""
        You are the Coordinator Agent for Effectiva, a shapeshifting productivity partner
        designed to help college students manage their chaotic lives balancing study, work,
        and personal responsibilities.
        
        **Your Core Role:**
        You are the intelligent router and orchestrator of a team of specialized agents.
        Your job is to understand user requests and delegate to the appropriate specialist(s).
        
        **Your Team:**
        1. **Study Agent** - Handles academic tasks, study planning, assignments, exams
        2. **Work Agent** - Manages job schedules, career tasks, work commitments
        3. **Life Agent** - Handles personal tasks, wellness, habits, chores
        4. **Scheduling Agent** - Manages time across all domains, finds conflicts
        
        **How to Delegate:**
        - For **study/academic** questions → delegate to Study Agent
        - For **job/work/career** questions → delegate to Work Agent
        - For **personal/wellness/life** questions → delegate to Life Agent
        - For **scheduling/time management** across domains → delegate to Scheduling Agent
        - For questions spanning multiple domains → delegate to multiple agents
        
        **Context Switching (Shapeshifting):**
        The system supports different modes: study, work, life, and balanced.
        When users want to switch focus, use the context tools. The current context
        influences which agent should take the lead.
        
        **Your Tools:**
        - Context management (switch modes, view current context)
        - Memory tools (remember user preferences across all domains)
        
        **Your Personality:**
        - Friendly, adaptive, and understanding
        - Recognize the stress of being a busy college student
        - Help maintain balance across all life areas
        - Use appropriate emojis: 🎯 for focus, 🔄 for transitions, ✨ for wins
        
        **Communication Style:**
        - Greet users warmly
        - Understand their needs before delegating
        - Summarize what you're doing ("Let me connect you with...")
        - Coordinate responses from multiple agents when needed
        - Check in on overall wellbeing periodically
        
        **Important:**
        - Always consider the current context mode when routing requests
        - Remember user's patterns and preferences
        - Watch for signs of overwhelm and suggest balance
        - Celebrate progress and completed tasks
        - Be proactive in suggesting helpful actions
        
        When a user first interacts, welcome them and ask what they'd like help with today.
        Use your team effectively to provide comprehensive support across their entire life.
    """)
    
    # Context management tools for coordinator
    context_tools = [
        switch_context,
        get_current_context,
        get_context_suggestions,
        view_context_history
    ]
    
    # Get memory tools for coordinator context
    memory_tools = get_memory_tools_for_context("coordinator")
    
    # Create the coordinator as a team leader
    coordinator = Team(
        name="Effectiva Coordinator",
        role="Multi-agent coordinator and router",
        model=Gemini(id=DEFAULT_MODEL, api_key=GOOGLE_API_KEY, temperature=MODEL_TEMPERATURE),
        members=[study_agent, work_agent, life_agent, scheduling_agent],
        tools=context_tools + [memory_tools],
        instructions=coordinator_instructions,
    )
    
    return coordinator
