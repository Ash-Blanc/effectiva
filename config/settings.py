"""Configuration settings for Effectiva AI Agent System."""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# API Keys - Should be set as environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Optional

# Memory Configuration
MEMORY_DB_PATH = os.getenv(
    "MEMORY_DB_PATH", 
    str(BASE_DIR / "effectiva_memory.db")
)
MEMORY_DB_URL = f"sqlite:///{MEMORY_DB_PATH}"

# Memory Namespaces
NAMESPACES = {
    "study": "effectiva:study",
    "work": "effectiva:work", 
    "life": "effectiva:life",
    "scheduling": "effectiva:scheduling",
    "coordinator": "effectiva:coordinator"
}

# LLM Configuration
DEFAULT_MODEL_PROVIDER = "google"
DEFAULT_MODEL = "gemini-2.5-pro"
MODEL_TEMPERATURE = 0.7
MAX_TOKENS = 2048

# Agent Configuration
AGENT_CONFIG = {
    "show_tool_calls": True,
    "markdown": True,
    "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true"
}

# AgentUI Configuration  
UI_CONFIG = {
    "title": "Effectiva • Shapeshifting Study Partner",
    "theme": "dark",
    "show_logs": True,
    "markdown": True,
    "port": int(os.getenv("PORT", "3001"))
}

# Context Modes
CONTEXT_MODES = ["study", "work", "life", "balanced"]

# Task Priorities
TASK_PRIORITIES = ["low", "medium", "high", "urgent"]
