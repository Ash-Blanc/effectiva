"""Coordinator agent that orchestrates the multi-agent team."""
import langwatch

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
from tools.quick_capture import (
    quick_add_task, quick_note, quick_reminder,
    quick_energy_check, get_recent_captures, process_natural_capture
)
from tools.time_management import (
    suggest_optimal_time_for_task, create_energy_aware_schedule
)
from config.settings import (
    DEFAULT_MODEL,
    MODEL_TEMPERATURE,
    AGENT_CONFIG,
    GOOGLE_API_KEY
)
from memory.memory_manager import get_memory_tools_for_context
from dspy_programs.intent_classifier import classify_intent
from integrations.whatsapp import log_whatsapp_message
from tools.bca_crisis_tools import handle_bca_crisis
from tools.bca_day_planner import handle_bca_day


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
    
    # Get coordinator prompt from LangWatch
    prompt = langwatch.prompts.get("coordinator")
    coordinator_instructions = prompt.prompt
    
    # Context management and quick capture tools for coordinator
    context_tools = [
        switch_context,
        get_current_context,
        get_context_suggestions,
        view_context_history,
        # Quick capture tools (essential for phone-based productivity)
        quick_add_task,
        quick_note,
        quick_reminder,
        quick_energy_check,
        get_recent_captures,
        process_natural_capture,
        # Energy-aware scheduling (addresses core productivity barrier)
        suggest_optimal_time_for_task,
        create_energy_aware_schedule,
    ]

    # Intelligence tools (callable by the coordinator LLM)
    intelligence_tools = [
        classify_intent,
        log_whatsapp_message,
        handle_bca_crisis,
        handle_bca_day,
    ]

    # Get memory tools for coordinator context
    memory_tools = get_memory_tools_for_context("coordinator")

    # Create the coordinator as a team leader
    coordinator = Team(
        name="Effectiva Coordinator",
        role="Multi-agent coordinator and router",
        model=Gemini(id=DEFAULT_MODEL, api_key=GOOGLE_API_KEY, temperature=MODEL_TEMPERATURE),
        members=[study_agent, work_agent, life_agent, scheduling_agent],
        tools=context_tools + intelligence_tools + [memory_tools],
        instructions=coordinator_instructions,
    )
    
    return coordinator
