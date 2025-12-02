# Effectiva User Guide

## Overview
Effectiva is a multi-agent system designed to help students manage their academic, work, and personal lives. It uses a team of specialized agents:

- **Study Agent**: Academic planning, assignments, exams.
- **Work Agent**: Job schedules, career planning.
- **Life Agent**: Personal habits, wellness, chores.
- **Scheduling Agent**: Time management, conflict resolution.
- **Coordinator Agent**: Orchestrates the team.

## Key Features

### 🧠 Intelligent Reasoning
Agents now "think" before they act. You might see a reasoning step in the logs where the agent analyzes your request, plans a response, and selects the right tools.

### ⚡ Optimized Performance
- **Toon Format**: Communication is compressed to save tokens and speed up responses.
- **DSPy Optimization**: Agents learn from interactions to improve their instructions over time.

### 🛠️ Built-in Tools
Agents have access to powerful tools:
- **Web Search**: For real-time information.
- **Calculator**: For quick math.
- **Calendar**: For scheduling.
- **File Operations**: For managing notes and documents.

## How to Use

### Starting the System
Run the main application:
```bash
uv run main.py
```
Access the UI at `http://localhost:3001` (or the port specified in logs).

### Interacting with Agents
- **Study Help**: "I have a math exam on Friday. Help me plan."
- **Work/Life Balance**: "I'm working 20 hours this week and have 3 assignments. How do I fit it all in?"
- **Crisis Mode**: "I'm 5 days behind on everything. Help!"

### Managing Configuration
You can enable/disable features via the API:
- **Toggle Toon Format**: `PATCH /api/toon/config/{agent_name}/toggle`
- **Register New Tools**: `POST /api/tools/register/{tool_key}`

## Troubleshooting
- **Rate Limits**: If you see "Rate limit exceeded", wait a minute before sending more requests.
- **Tool Errors**: If a tool fails, the agent will retry automatically. Check the logs for details.
