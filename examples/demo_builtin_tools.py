"""Test script to demonstrate built-in tools integration."""
from database import init_db, SessionLocal
from builtin_tools_service import BuiltInToolsService
from logger import logger


def test_builtin_tools():
    """Test built-in tools registration and management."""
    logger.info("=== Testing Built-in Tools Integration ===\n")
    
    # Initialize database
    init_db()
    db = SessionLocal()
    
    try:
        # 1. List available tools
        logger.info("--- Available Built-in Tools ---")
        for key, info in BuiltInToolsService.AVAILABLE_TOOLS.items():
            logger.info(f"  • {info['name']} ({info['category']})")
            logger.info(f"    {info['description']}")
        logger.info("")
        
        # 2. Register all tools
        logger.info("--- Registering All Tools ---")
        tools = BuiltInToolsService.register_all_tools(db)
        logger.info(f"✓ Registered {len(tools)} tools\n")
        
        # 3. Get tools by category
        logger.info("--- Tools by Category ---")
        categories = ["web", "utility", "file", "code", "system"]
        for category in categories:
            cat_tools = BuiltInToolsService.get_tools_by_category(db, category)
            if cat_tools:
                logger.info(f"{category.upper()}: {len(cat_tools)} tools")
                for t in cat_tools:
                    logger.info(f"  • {t.name}")
        logger.info("")
        
        # 4. Get recommended tools for each agent type
        logger.info("--- Recommended Tools by Agent Type ---")
        agent_types = ["study", "work", "life", "scheduling", "coordinator"]
        for agent_type in agent_types:
            recommended = BuiltInToolsService.get_safe_tools_for_agent(agent_type)
            logger.info(f"{agent_type.upper()} Agent: {', '.join(recommended)}")
        logger.info("")
        
        # 5. Test tool instantiation (if available)
        logger.info("--- Testing Tool Instantiation ---")
        test_tools = ["datetime_tools", "calculator"]
        
        for tool_key in test_tools:
            logger.info(f"Attempting to load: {tool_key}")
            try:
                tool_instance = BuiltInToolsService.get_tool_instance(tool_key)
                if tool_instance:
                    logger.info(f"✓ Successfully loaded {tool_key}")
                else:
                    logger.info(f"⚠ Tool {tool_key} not available (may need agno installation)")
            except Exception as e:
                logger.info(f"⚠ Could not instantiate {tool_key}: {str(e)[:100]}")
        logger.info("")
        
        # 6. Toggle tool status
        logger.info("--- Testing Tool Toggle ---")
        first_tool = tools[0] if tools else None
        if first_tool:
            logger.info(f"Toggling {first_tool.name}...")
            
            # Deactivate
            BuiltInToolsService.toggle_tool(db, first_tool.id, False)
            logger.info(f"✓ Deactivated {first_tool.name}")
            
            # Reactivate
            BuiltInToolsService.toggle_tool(db, first_tool.id, True)
            logger.info(f"✓ Reactivated {first_tool.name}")
        logger.info("")
        
        # 7. Summary
        logger.info("=== Summary ===")
        active_tools = BuiltInToolsService.get_active_tools(db)
        logger.info(f"Total Active Tools: {len(active_tools)}")
        logger.info(f"Categories: {', '.join(categories)}")
        logger.info("✅ Built-in tools integration ready!\n")
        
        # 8. API Usage Examples
        logger.info("--- API Usage Examples ---")
        logger.info("Register all tools:")
        logger.info("  POST /api/tools/register-all")
        logger.info("")
        logger.info("Get recommended tools for study agent:")
        logger.info("  GET /api/tools/recommended/study")
        logger.info("")
        logger.info("List all active tools:")
        logger.info("  GET /api/tools")
        logger.info("")
        logger.info("Get tools by category:")
        logger.info("  GET /api/tools/category/web")
        logger.info("")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    test_builtin_tools()
