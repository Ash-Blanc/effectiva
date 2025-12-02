"""
Scenario tests for Effectiva scheduling agent.
Tests end-to-end agent functionality for cross-domain time management and conflict resolution.
"""

import pytest
import asyncio
from scenario import AgentAdapter, AgentInput, run, JudgeAgent, UserSimulatorAgent
from agents.scheduling_agent import create_scheduling_agent


class SchedulingAgentAdapter(AgentAdapter):
    """Adapter for Effectiva scheduling agent."""

    def __init__(self):
        self.agent = create_scheduling_agent()

    async def call(self, input: AgentInput):
        """Process input through the scheduling agent."""
        user_message = input.last_new_user_message_str()
        response = await self.agent.run(user_message)
        return response.content


@pytest.fixture
def scheduling_agent_adapter():
    """Create scheduling agent adapter for testing."""
    return SchedulingAgentAdapter()


@pytest.mark.asyncio
async def test_cross_domain_scheduling(scheduling_agent_adapter):
    """Test that scheduling agent manages time across study, work, and life domains."""
    result = await run(
        name="Cross-Domain Scheduling",
        description="Test scheduling agent balances multiple life domains",
        agents=[
            scheduling_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response considers study, work, and personal time",
                               "Shows conflict resolution between domains",
                               "Creates balanced schedule with realistic time allocation"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_conflict_resolution(scheduling_agent_adapter):
    """Test that scheduling agent resolves scheduling conflicts."""
    result = await run(
        name="Conflict Resolution",
        description="Test scheduling agent identifies and resolves time conflicts",
        agents=[
            scheduling_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response identifies conflicting commitments",
                               "Provides resolution options or alternatives",
                               "Prioritizes tasks appropriately"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_deadline_prioritization(scheduling_agent_adapter):
    """Test that scheduling agent prioritizes tasks by deadlines."""
    result = await run(
        name="Deadline Prioritization",
        description="Test scheduling agent organizes tasks by urgency and deadlines",
        agents=[
            scheduling_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response prioritizes tasks by deadlines",
                               "Shows time estimation for tasks",
                               "Creates realistic timelines"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_free_time_optimization(scheduling_agent_adapter):
    """Test that scheduling agent finds and utilizes free time slots."""
    result = await run(
        name="Free Time Optimization",
        description="Test scheduling agent identifies free slots and suggests usage",
        agents=[
            scheduling_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response identifies available time slots",
                               "Suggests productive use of free time",
                               "Considers energy levels and task types"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_bca_scheduling_crisis(scheduling_agent_adapter):
    """Test that scheduling agent handles BCA crisis scheduling."""
    result = await run(
        name="BCA Scheduling Crisis",
        description="Test scheduling agent creates catch-up plans for academic crises",
        agents=[
            scheduling_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response creates micro-schedules for catch-up",
                               "Breaks down large tasks into manageable pieces",
                               "Includes realistic time blocks and breaks"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"