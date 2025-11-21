"""Memory management using MemoriSDK for persistent, context-aware agent memory."""
from agno.tools.memori import MemoriTools
from config.settings import MEMORY_DB_URL, NAMESPACES


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
    """
    Convenience function to get memory tools for a context.
    
    Args:
        context: Agent context name
        
    Returns:
        MemoriTools instance
    """
    return memory_manager.get_memory_tools(context)
