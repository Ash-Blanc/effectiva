"""
Scenario tests for Effectiva work agent.
Tests end-to-end agent functionality for job tasks and career management.
"""

import pytest
import asyncio
from scenario import AgentAdapter, AgentInput, run, JudgeAgent, UserSimulatorAgent
from agents.work_agent import create_work_agent


class WorkAgentAdapter(AgentAdapter):
    """Adapter for Effectiva work agent."""

    def __init__(self):
        self.agent = create_work_agent()

    async def call(self, input: AgentInput):
        """Process input through the work agent."""
        user_message = input.last_new_user_message_str()
        response = await self.agent.run(user_message)
        return response.content


@pytest.fixture
def work_agent_adapter():
    """Create work agent adapter for testing."""
    return WorkAgentAdapter()


@pytest.mark.asyncio
async def test_job_task_management(work_agent_adapter):
    """Test that work agent manages job-related tasks effectively."""
    result = await run(
        name="Job Task Management",
        description="Test work agent creates and prioritizes work tasks",
        agents=[
            work_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response creates specific work-related tasks",
                               "Tasks include deadlines or priorities",
                               "Shows work-life balance considerations"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_shift_scheduling(work_agent_adapter):
    """Test that work agent handles shift scheduling."""
    result = await run(
        name="Shift Scheduling",
        description="Test work agent manages work schedules and shifts",
        agents=[
            work_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response addresses shift times and durations",
                               "Considers conflicts with other commitments",
                               "Provides scheduling recommendations"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_career_planning(work_agent_adapter):
    """Test that work agent provides career guidance."""
    result = await run(
        name="Career Planning",
        description="Test work agent offers career development advice",
        agents=[
            work_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response includes career development suggestions",
                               "Addresses skill development or advancement",
                               "Considers work goals and aspirations"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_work_life_balance(work_agent_adapter):
    """Test that work agent maintains work-life balance."""
    result = await run(
        name="Work-Life Balance",
        description="Test work agent helps balance work and personal life",
        agents=[
            work_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response considers personal time and boundaries",
                               "Addresses potential burnout or overwork",
                               "Suggests balance strategies"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"