"""
Scenario tests for Effectiva study agent.
Tests end-to-end agent functionality for academic planning and crisis management.
"""

import pytest
import asyncio
from scenario import AgentAdapter, AgentInput, run, JudgeAgent, UserSimulatorAgent
from agents.study_agent import create_study_agent


class StudyAgentAdapter(AgentAdapter):
    """Adapter for Effectiva study agent."""

    def __init__(self):
        self.agent = create_study_agent()

    async def call(self, input: AgentInput):
        """Process input through the study agent."""
        user_message = input.last_new_user_message_str()
        response = await self.agent.run(user_message)
        return response.content


@pytest.fixture
def study_agent_adapter():
    """Create study agent adapter for testing."""
    return StudyAgentAdapter()


@pytest.mark.asyncio
async def test_academic_planning(study_agent_adapter):
    """Test that study agent creates effective study plans."""
    result = await run(
        name="Academic Planning",
        description="Test study agent creates comprehensive study plans for exams",
        agents=[
            study_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response includes specific study schedule with time blocks",
                               "Plan addresses multiple subjects or topics",
                               "Includes breaks and realistic time estimates"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_task_creation(study_agent_adapter):
    """Test that study agent creates and manages academic tasks."""
    result = await run(
        name="Task Management",
        description="Test study agent creates tasks for assignments and deadlines",
        agents=[
            study_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response creates specific, actionable tasks",
                               "Tasks include deadlines or time estimates",
                               "Shows task organization or prioritization"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_bca_crisis_handling(study_agent_adapter):
    """Test that study agent handles crisis situations effectively."""
    result = await run(
        name="BCA Crisis Response",
        description="Test study agent provides micro-plans for students behind on classes",
        agents=[
            study_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response creates small, manageable tasks",
                               "Plan includes realistic time estimates",
                               "Shows empathy and encourages small wins",
                               "Addresses specific crisis elements (missed classes, assignments)"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"


@pytest.mark.asyncio
async def test_study_schedule_optimization(study_agent_adapter):
    """Test that study agent optimizes study schedules."""
    result = await run(
        name="Schedule Optimization",
        description="Test study agent suggests optimal study times and techniques",
        agents=[
            study_agent_adapter,
            UserSimulatorAgent(),
            JudgeAgent(criteria=["Response suggests specific study techniques",
                               "Includes time management recommendations",
                               "Considers energy levels or optimal study times"])
        ]
    )

    assert result.success, f"Test failed: {result.reasoning}"