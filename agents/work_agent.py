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
    # Get work agent prompt from LangWatch
    prompt = langwatch.prompts.get("work_agent")
    instructions = prompt.prompt
    
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
