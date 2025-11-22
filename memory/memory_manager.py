"""Memory management using MemoriSDK for persistent, context-aware agent memory."""
from agno.tools.memori import MemoriTools
from config.settings import MEMORY_DB_URL, NAMESPACES
from typing import Any, Dict, List, Optional

from schemas.toon_models import (
    Task,
    ScheduleBlock,
    StudentProfile,
    CrisisEpisode,
    task_to_toon,
    schedule_block_to_toon,
    student_profile_to_toon,
    crisis_episode_to_toon,
)


class MemoryManager:
    """Manages memory for different agent contexts using MemoriSDK."""
    
    def __init__(self):
        """Initialize memory tools for each agent namespace."""
        self.memory_tools = {}
        self._initialize_memory_tools()
    
    def _initialize_memory_tools(self):
        """Create MemoriTools instances for each agent namespace."""
        for context, namespace in NAMESPACES.items():
            self.memory_tools[context] = MemoriTools(
                database_connect=MEMORY_DB_URL,
                namespace=namespace,
            )
    
    def get_memory_tools(self, context: str) -> MemoriTools:
        """
        Get memory tools for a specific context.
        
        Args:
            context: Agent context (study, work, life, scheduling, coordinator)
            
        Returns:
            MemoriTools instance for the specified context
        """
        if context not in self.memory_tools:
            raise ValueError(
                f"Invalid context: {context}. "
                f"Valid contexts: {list(self.memory_tools.keys())}"
            )
        return self.memory_tools[context]


# Global memory manager instance
memory_manager = MemoryManager()


def get_memory_tools_for_context(context: str) -> MemoriTools:
    """Convenience function to get memory tools for a context."""
    return memory_manager.get_memory_tools(context)


# ---------------------------------------------------------------------------
# High-level structured memory helpers
# ---------------------------------------------------------------------------


def remember_fact(context: str, key: str, value: str, tags: Optional[List[str]] = None) -> str:
    """Store a simple key/value fact in Memori for a given context.

    This is intentionally stringly-typed; higher-level helpers below
    use Toon to store structured payloads.
    """

    tools = get_memory_tools_for_context(context)
    tags = tags or []
    # We use `key` as the memory title and store `value` as content.
    tools.add_memory(title=key, content=value, tags=tags)
    return f"✓ Remembered fact `{key}` for {context}"


def log_event(context: str, event_type: str, payload: Dict[str, Any]) -> str:
    """Log an event with a given type and JSON-like payload.

    Use this for episodic information like study sessions, crisis
    assessments, or WhatsApp message events.
    """

    tools = get_memory_tools_for_context(context)
    title = f"event:{event_type}"
    # We rely on Memori's own storage; payload is stringified here.
    tools.add_memory(title=title, content=str(payload), tags=[event_type])
    return f"✓ Logged event `{event_type}` for {context}"


# --- Toon-specialized helpers ------------------------------------------------


def store_task(context: str, task: Task, tags: Optional[List[str]] = None) -> str:
    tools = get_memory_tools_for_context(context)
    toon_str = task_to_toon(task)
    title = f"task:{task.id}"
    tools.add_memory(title=title, content=toon_str, tags=(tags or ["task"]))
    return f"✓ Stored task {task.id} in {context}"


def store_schedule_block(context: str, block: ScheduleBlock, tags: Optional[List[str]] = None) -> str:
    tools = get_memory_tools_for_context(context)
    toon_str = schedule_block_to_toon(block)
    title = f"schedule:{block.label}"
    tools.add_memory(title=title, content=toon_str, tags=(tags or ["schedule"]))
    return f"✓ Stored schedule block `{block.label}` in {context}"


def store_student_profile(context: str, profile: StudentProfile, tags: Optional[List[str]] = None) -> str:
    tools = get_memory_tools_for_context(context)
    toon_str = student_profile_to_toon(profile)
    title = "student_profile"
    tools.add_memory(title=title, content=toon_str, tags=(tags or ["profile"]))
    return f"✓ Stored student profile for {context}"


def store_crisis_episode(context: str, episode: CrisisEpisode, tags: Optional[List[str]] = None) -> str:
    tools = get_memory_tools_for_context(context)
    toon_str = crisis_episode_to_toon(episode)
    title = f"crisis:{episode.severity}"
    tools.add_memory(title=title, content=toon_str, tags=(tags or ["crisis"]))
    return f"✓ Stored crisis episode ({episode.severity}) for {context}"
