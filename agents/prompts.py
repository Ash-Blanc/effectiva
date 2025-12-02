"""Standardized prompt templates for Effectiva agents."""
from textwrap import dedent
from typing import Optional

class BasePromptTemplate:
    """Base template for agent system prompts using XML structure and CoT."""
    
    @staticmethod
    def build(
        role: str,
        personality: str,
        responsibilities: list[str],
        approach: list[str],
        tools_description: str,
        communication_style: list[str],
        additional_instructions: Optional[str] = None
    ) -> str:
        """
        Build a standardized system prompt.
        """
        responsibilities_str = "\n".join([f"- {r}" for r in responsibilities])
        approach_str = "\n".join([f"- {a}" for a in approach])
        style_str = "\n".join([f"- {s}" for s in communication_style])
        
        prompt = dedent(f"""
        <agent_profile>
        <role>{role}</role>
        <personality>{personality}</personality>
        </agent_profile>

        <responsibilities>
        {responsibilities_str}
        </responsibilities>

        <approach>
        {approach_str}
        </approach>

        <tools_available>
        {tools_description}
        </tools_available>

        <communication_style>
        {style_str}
        </communication_style>

        <reasoning_framework>
        You are an intelligent agent that thinks before acting.
        When presented with a complex request, you MUST use the following reasoning process:
        1. **Analyze**: Understand the user's intent, context, and constraints.
        2. **Plan**: Formulate a step-by-step plan to address the request.
        3. **Tool Selection**: Identify which tools (if any) are needed for each step.
        4. **Execution**: Execute the plan, using tools as necessary.
        5. **Reflection**: Verify if the result meets the user's needs.
        
        You should output your reasoning process in a `<thought>` block before your final response if the task is complex.
        </reasoning_framework>
        """)
        
        if additional_instructions:
            prompt += dedent(f"""
            <additional_instructions>
            {additional_instructions}
            </additional_instructions>
            """)
            
        return prompt.strip()
