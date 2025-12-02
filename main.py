"""Main entry point for Effectiva AI Agent System."""
import langwatch

from agno.os import AgentOS
from agents.coordinator import create_coordinator_agent
from config.settings import UI_CONFIG, LANGWATCH_API_KEY

# LangWatch initialization (if needed)
# Note: LangWatch may not require explicit initialization in newer versions
try:
    if hasattr(langwatch, 'init'):
        langwatch.init(api_key=LANGWATCH_API_KEY)
except Exception as e:
    print(f"⚠️ LangWatch initialization skipped: {e}")
    # LangWatch prompts can still be accessed without explicit init

# Create the coordinator agent with the full team
agent = create_coordinator_agent()

# AgentOS setup
# We pass both the team (for coordination) and individual agents (for direct access/UI)
agent_os = AgentOS(
    teams=[agent],
    agents=agent.members if hasattr(agent, "members") else []
)
app = agent_os.get_app()

# Core Integrations (Conditional based on available API keys)
from integrations.google_calendar import (
    list_calendars, get_events as google_get_events, create_event as google_create_event,
    find_free_slots as google_find_free_slots
)

# Discord Integration (Primary social platform focus)
from integrations.discord import send_message as discord_send, get_channel_messages as discord_get_messages

# WhatsApp Integration (Optional - only if API keys available and tools initialized)
whatsapp_tools = []
try:
    from integrations.whatsapp import send_message as whatsapp_send, send_template_message as whatsapp_template
    # Only add if the tools were successfully initialized (not None)
    if whatsapp_send is not None and whatsapp_template is not None:
        whatsapp_tools = [whatsapp_send, whatsapp_template]
        print("✅ WhatsApp integration enabled")
    else:
        print("⚠️ WhatsApp integration disabled (tools not initialized)")
except ImportError as e:
    print(f"⚠️ WhatsApp integration not available: {e}")

# Add essential productivity tools to the coordinator team
productivity_tools = [
    # Discord (primary social platform for study communities)
    discord_send,
    discord_get_messages,
    # Google Calendar (essential for time management)
    list_calendars,
    google_get_events,
    google_create_event,
    google_find_free_slots,
] + whatsapp_tools  # Add WhatsApp only if available

# Extend the team's tools with social and productivity integrations
agent.tools.extend(productivity_tools)

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 Starting Effectiva - Your Shapeshifting Study Partner")
    print("="*60)
    print(f"\n📱 AgentUI running on: http://localhost:{UI_CONFIG['port']}")
    print("\n💡 Features:")
    print("   • Multi-agent team (Study, Work, Life, Scheduling)")
    print("   • Persistent memory across sessions")
    print("   • Context switching (study/work/life/balanced modes)")
    print("   • Task & calendar management")
    print("\n💬 Just start chatting to get help with anything!")
    print("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=UI_CONFIG["port"])
