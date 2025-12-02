"""
Scenario tests for Effectiva life agent.
Tests end-to-end agent functionality for personal tasks and wellness management.
"""

import pytest
import asyncio
from scenario import AgentAdapter, AgentInput, run, JudgeAgent, UserSimulatorAgent
from agents.life_agent import create_life_agent


class LifeAgentAdapter(AgentAdapter):
    """Adapter for Effectiva life agent."""

    def __init__(self):
        self.agent = create_life_agent()

    async def call(self, input: AgentInput):
        """Process input through the life agent."""
        user_message = input.last_new_user_message_str()
        response = await self.agent.run(user_message)
        return response.content


@pytest.fixture
def life_agent_adapter():
    """Create life agent adapter for testing."""
    return LifeAgentAdapter()


@pytest.mark.asyncio
async def test_personal_task_management(life_agent_adapter):
    """Test that life agent manages personal tasks and chores."""
    result = await run(
        name="Personal Task Management",
        description="Test life agent creates and organizes personal tasks",
        agents=[
            life_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response creates specific personal tasks",
                               "Tasks are realistic and achievable",
                               "Shows organization or prioritization of daily life"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_wellness_support(life_agent_adapter):
    """Test that life agent provides wellness and self-care guidance."""
    result = await run(
        name="Wellness Support",
        description="Test life agent offers wellness and self-care recommendations",
        agents=[
            life_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response addresses mental or physical wellness",
                               "Includes self-care suggestions",
                               "Shows empathy and encouragement"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_habit_tracking(life_agent_adapter):
    """Test that life agent helps with habit formation and tracking."""
    result = await run(
        name="Habit Tracking",
        description="Test life agent assists with building and maintaining habits",
        agents=[
            life_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response includes habit-building strategies",
                               "Suggests tracking methods or routines",
                               "Provides realistic habit formation advice"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_relationship_balance(life_agent_adapter):
    """Test that life agent helps balance relationships and social life."""
    result = await run(
        name="Relationship Balance",
        description="Test life agent addresses social connections and relationships",
        agents=[
            life_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response considers social connections",
                               "Addresses relationship maintenance",
                               "Suggests balance between social and personal time"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"