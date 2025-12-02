"""Configuration settings for Effectiva AI Agent System."""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# API Keys - Should be set as environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # Optional
LANGWATCH_API_KEY = os.getenv("LANGWATCH_API_KEY")

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

# Social Integration Configurations
def get_whatsapp_config():
    """Get WhatsApp Business API configuration."""
    return {
        "access_token": os.getenv("WHATSAPP_ACCESS_TOKEN"),
        "phone_number_id": os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    }

def get_discord_config():
    """Get Discord bot configuration."""
    return {
        "bot_token": os.getenv("DISCORD_BOT_TOKEN"),
        "default_channel_id": os.getenv("DISCORD_DEFAULT_CHANNEL_ID"),
    }

def get_linkedin_config():
    """Get LinkedIn API configuration."""
    return {
        "access_token": os.getenv("LINKEDIN_ACCESS_TOKEN"),
        "person_urn": os.getenv("LINKEDIN_PERSON_URN"),
    }
