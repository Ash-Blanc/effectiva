"""Main entry point for Effectiva AI Agent System."""
from agno.os import AgentOS
from agents.coordinator import create_coordinator_agent
from config.settings import UI_CONFIG

# Create the coordinator agent with the full team
agent = create_coordinator_agent()

# AgentOS setup
agent_os = AgentOS(teams=[agent])
app = agent_os.get_app()

# TODO: WhatsApp integration can be added later
# from integrations.whatsapp import router as whatsapp_router
# app.include_router(whatsapp_router)

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
