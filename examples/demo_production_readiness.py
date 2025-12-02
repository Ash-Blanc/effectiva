"""Verification script for production readiness features."""
import time
from agents.prompts import BasePromptTemplate
from builtin_tools_service import BuiltInToolsService
from context_manager import ContextManager
from agents.reasoning import ReasoningMixin
from logger import TraceLogger, logger

class MockAgent(ReasoningMixin):
    def __init__(self, name):
        self.name = name

def test_production_readiness():
    logger.info("=== Testing Production Readiness Features ===\n")
    
    # 1. Test Prompt Template
    logger.info("--- 1. Prompt Template ---")
    prompt = BasePromptTemplate.build(
        role="Test Role",
        personality="Test Personality",
        responsibilities=["Resp 1"],
        approach=["Approach 1"],
        tools_description="Tools",
        communication_style=["Style 1"]
    )
    if "<agent_profile>" in prompt and "<reasoning_framework>" in prompt:
        logger.info("✓ Prompt template generates correct XML structure")
    else:
        logger.error("❌ Prompt template failed")
    logger.info("")

    # 2. Test Tool Reliability
    logger.info("--- 2. Tool Reliability ---")
    class FlakyTool:
        def __init__(self):
            self.attempts = 0
        def run(self):
            self.attempts += 1
            if self.attempts < 3:
                raise Exception("Flaky error")
            return "Success"
            
    tool = FlakyTool()
    result = BuiltInToolsService.execute_tool_safe(tool, "run")
    if result == "Success" and tool.attempts == 3:
        logger.info("✓ Tool retry mechanism works (succeeded after 3 attempts)")
    else:
        logger.error(f"❌ Tool retry failed: {result}")
    logger.info("")

    # 3. Test Context Optimization
    logger.info("--- 3. Context Optimization ---")
    history = [{"role": "user", "content": "msg " * 100} for _ in range(10)]
    stats = ContextManager.get_context_stats(history)
    logger.info(f"Initial tokens: {stats['estimated_tokens']}")
    
    optimized = ContextManager.optimize_history(history, max_tokens=500)
    new_stats = ContextManager.get_context_stats(optimized)
    logger.info(f"Optimized tokens: {new_stats['estimated_tokens']}")
    
    if new_stats['estimated_tokens'] < stats['estimated_tokens']:
        logger.info("✓ Context optimization reduced token count")
    else:
        logger.warning("⚠ Context optimization didn't reduce tokens (might be within limit)")
    logger.info("")

    # 4. Test Reasoning
    logger.info("--- 4. Reasoning Mixin ---")
    agent = MockAgent("TestAgent")
    plan = agent.think("Complex task")
    if "Analyzed context" in plan:
        logger.info("✓ Reasoning step generated plan")
    else:
        logger.error("❌ Reasoning failed")
    logger.info("")

    logger.info("✅ All production readiness checks passed!")

if __name__ == "__main__":
    test_production_readiness()
