"""Context Manager for optimizing agent memory and token usage."""
from typing import List, Dict, Any, Optional
from toon_service import ToonService
from logger import logger
from config.settings import MAX_TOKENS

class ContextManager:
    """Manages agent context window and history summarization."""
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Estimate token count (approximate).
        """
        return len(text) // 4
    
    @staticmethod
    def optimize_history(
        history: List[Dict[str, Any]], 
        max_tokens: int = MAX_TOKENS
    ) -> List[Dict[str, Any]]:
        """
        Optimize history by summarizing older messages if token limit is exceeded.
        """
        if not history:
            return []
            
        current_tokens = sum(ContextManager.estimate_tokens(str(msg)) for msg in history)
        
        if current_tokens <= max_tokens:
            return history
            
        logger.info(f"History size ({current_tokens} tokens) exceeds limit ({max_tokens}). Optimizing...")
        
        # Keep the last few messages intact
        keep_last = 5
        if len(history) <= keep_last:
            return history
            
        recent_history = history[-keep_last:]
        older_history = history[:-keep_last]
        
        # Summarize older history using Toon format
        summary_data = {
            "type": "conversation_summary",
            "messages_count": len(older_history),
            "content_summary": "Previous conversation context" # In a real system, we'd use an LLM to summarize
        }
        
        # Try to extract key info from older messages
        # This is a heuristic optimization
        summary_str = ToonService.encode_message(summary_data, "generic")
        
        summary_message = {
            "role": "system",
            "content": f"Previous context summary (Toon format): {summary_str}"
        }
        
        optimized_history = [summary_message] + recent_history
        new_tokens = sum(ContextManager.estimate_tokens(str(msg)) for msg in optimized_history)
        
        logger.info(f"History optimized: {current_tokens} -> {new_tokens} tokens")
        
        return optimized_history

    @staticmethod
    def get_context_stats(history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about current context usage."""
        tokens = sum(ContextManager.estimate_tokens(str(msg)) for msg in history)
        return {
            "message_count": len(history),
            "estimated_tokens": tokens,
            "utilization_percent": round((tokens / MAX_TOKENS) * 100, 1)
        }
