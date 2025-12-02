"""Study agent specialized in academic tasks, learning, and study planning."""
import langwatch

from agents.base import BaseAgent
from tools.task_tools import (
    create_task, get_tasks, complete_task,
    update_task_priority, get_urgent_tasks
)
from tools.calendar_tools import add_event, get_events, find_free_slots
from tools.time_management import suggest_study_schedule, create_time_block
from tools.bca_crisis_tools import plan_bca_catchup
from tools.bca_day_planner import handle_bca_day
from tools.study_techniques import (
    generate_spaced_study_schedule,
    generate_active_recall_questions,
    recommend_study_technique_tool
)
from textwrap import dedent


def create_study_agent() -> BaseAgent:
    """
    Create the Study Agent specialized in academic tasks.
    
    Returns:
        BaseAgent instance configured as Study Agent
    """
    # Get study agent prompt from LangWatch with fallback
    try:
        prompt = langwatch.prompts.get("study_agent")
        instructions = prompt.prompt
    except Exception as e:
        print(f"⚠️ Failed to load study_agent prompt from LangWatch: {e}")
        # Fallback to basic instructions
        instructions = """
        You are a Study Agent specialized in academic tasks and learning.

        Your role is to help students with:
        - Creating effective study plans and schedules
        - Managing assignments and deadlines
        - Providing study techniques and learning strategies
        - Organizing academic tasks and priorities

        Be encouraging, practical, and focused on student success.
        """
    
    tools = [
        create_task,
        get_tasks,
        complete_task,
        update_task_priority,
        get_urgent_tasks,
        add_event,
        get_events,
        find_free_slots,
        suggest_study_schedule,
        create_time_block,
        plan_bca_catchup,
        handle_bca_day,
        # Advanced study techniques
        generate_spaced_study_schedule,
        generate_active_recall_questions,
        recommend_study_technique_tool,
    ]
    
    return BaseAgent(
        name="Study Agent",
        role="Academic assistant for students",
        context="study",
        instructions=instructions,
        tools=tools,
        add_memory=True
    )
