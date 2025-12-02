"""Life agent specialized in personal tasks, habits, wellness, and life management."""
import langwatch

from agents.base import BaseAgent
from tools.task_tools import create_task, get_tasks, complete_task
from tools.calendar_tools import add_event, get_events
from tools.time_management import suggest_break_schedule, create_time_block
from textwrap import dedent


def create_life_agent() -> BaseAgent:
    """
    Create the Life Agent specialized in personal life management.
    
    Returns:
        BaseAgent instance configured as Life Agent
    """
    # Get life agent prompt from LangWatch with fallback
    try:
        prompt = langwatch.prompts.get("life_agent")
        instructions = prompt.prompt
    except Exception as e:
        print(f"⚠️ Failed to load life_agent prompt from LangWatch: {e}")
        # Fallback to basic instructions
        instructions = """
        You are a Life Agent specialized in personal wellness and life management.

        Your role is to help students with:
        - Managing personal tasks and chores
        - Wellness and self-care routines
        - Habit formation and maintenance
        - Work-life balance and stress management

        Be supportive, understanding, and focused on holistic well-being.
        """
    
    tools = [
        create_task,
        get_tasks,
        complete_task,
        add_event,
        get_events,
        suggest_break_schedule,
        create_time_block
    ]
    
    return BaseAgent(
        name="Life Agent",
        role="Personal life and wellness assistant",
        context="life",
        instructions=instructions,
        tools=tools,
        add_memory=True
    )
