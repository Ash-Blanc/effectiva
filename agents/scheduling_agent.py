"""Scheduling agent specialized in cross-domain time management and conflict resolution."""
import langwatch

from agents.base import BaseAgent
from tools.calendar_tools import (
    add_event, get_events, find_free_slots,
    get_upcoming_events, delete_event
)
from tools.time_management import (
    create_time_block, suggest_study_schedule,
    calculate_time_needed, prioritize_tasks_by_deadline,
    suggest_break_schedule
)
from tools.bca_crisis_tools import plan_bca_catchup
from tools.bca_day_planner import plan_bca_day, handle_bca_day
from textwrap import dedent


def create_scheduling_agent() -> BaseAgent:
    """
    Create the Scheduling Agent specialized in time management.
    
    Returns:
        BaseAgent instance configured as Scheduling Agent
    """
    # Get scheduling agent prompt from LangWatch with fallback
    try:
        prompt = langwatch.prompts.get("scheduling_agent")
        instructions = prompt.prompt
    except Exception as e:
        print(f"⚠️ Failed to load scheduling_agent prompt from LangWatch: {e}")
        # Fallback to basic instructions
        instructions = """
        You are a Scheduling Agent specialized in time management and coordination.

        Your role is to help students with:
        - Cross-domain time allocation (study, work, life)
        - Conflict resolution between commitments
        - Optimal scheduling based on energy levels
        - Deadline prioritization and time blocking

        Be systematic, practical, and focused on efficient time use.
        """
    
    tools = [
        add_event,
        get_events,
        find_free_slots,
        get_upcoming_events,
        delete_event,
        create_time_block,
        suggest_study_schedule,
        calculate_time_needed,
        prioritize_tasks_by_deadline,
        suggest_break_schedule,
        plan_bca_catchup,
        plan_bca_day,
        handle_bca_day,
    ]
    
    return BaseAgent(
        name="Scheduling Agent",
        role="Time management and scheduling specialist",
        context="scheduling",
        instructions=instructions,
        tools=tools,
        add_memory=True
    )
