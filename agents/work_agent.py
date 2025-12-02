"""Work agent specialized in job-related tasks and career management."""
import langwatch

from agents.base import BaseAgent
from tools.task_tools import create_task, get_tasks, complete_task, get_urgent_tasks
from tools.calendar_tools import add_event, get_events, get_upcoming_events
from tools.time_management import create_time_block
from textwrap import dedent


def create_work_agent() -> BaseAgent:
    """
    Create the Work Agent specialized in job and career tasks.
    
    Returns:
        BaseAgent instance configured as Work Agent
    """
    # Get work agent prompt from LangWatch with fallback
    try:
        prompt = langwatch.prompts.get("work_agent")
        instructions = prompt.prompt
    except Exception as e:
        print(f"⚠️ Failed to load work_agent prompt from LangWatch: {e}")
        # Fallback to basic instructions
        instructions = """
        You are a Work Agent specialized in job-related tasks and career management.

        Your role is to help students with:
        - Managing part-time job schedules and shifts
        - Balancing work and academic responsibilities
        - Career planning and professional development
        - Work-life balance optimization

        Be practical, professional, and focused on sustainable work habits.
        """
    
    tools = [
        create_task,
        get_tasks,
        complete_task,
        get_urgent_tasks,
        add_event,
        get_events,
        get_upcoming_events,
        create_time_block
    ]
    
    return BaseAgent(
        name="Work Agent",
        role="Job and career management assistant",
        context="work",
        instructions=instructions,
        tools=tools,
        add_memory=True
    )
