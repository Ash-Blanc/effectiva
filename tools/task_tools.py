"""Task management tools for creating, tracking, and organizing student tasks."""
from datetime import datetime
from typing import Optional, List
import json


# Simple in-memory task storage (can be enhanced with DB later)
TASKS_STORE = {}


def create_task(
    title: str, 
    description: str = "",
    priority: str = "medium",
    category: str = "general",
    deadline: Optional[str] = None
) -> str:
    """
    Create a new task with priority and optional deadline.
    
    Args:
        title: Task title/summary
        description: Detailed task description
        priority: Task priority (low, medium, high, urgent)
        category: Task category (study, work, life, personal)
        deadline: Optional deadline in ISO format (YYYY-MM-DD)
    
    Returns:
        Confirmation message with task ID
    """
    task_id = f"task_{len(TASKS_STORE) + 1}_{datetime.now().timestamp()}"
    
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "deadline": deadline,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    
    TASKS_STORE[task_id] = task
    
    return f"✓ Task created: '{title}' (ID: {task_id}, Priority: {priority})"


def get_tasks(
    status: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None
) -> str:
    """
    Get list of tasks, optionally filtered by status, category, or priority.
    
    Args:
        status: Filter by status (pending, completed, all)
        category: Filter by category (study, work, life)
        priority: Filter by priority (low, medium, high, urgent)
    
    Returns:
        Formatted list of tasks
    """
    tasks = list(TASKS_STORE.values())
    
    # Apply filters
    if status and status != "all":
        tasks = [t for t in tasks if t["status"] == status]
    if category:
        tasks = [t for t in tasks if t["category"] == category]
    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    
    if not tasks:
        return "No tasks found matching the criteria."
    
    # Format output
    result = f"**Found {len(tasks)} task(s):**\n\n"
    for task in tasks:
        deadline_str = f" | Deadline: {task['deadline']}" if task['deadline'] else ""
        status_icon = "✓" if task['status'] == "completed" else "○"
        result += f"{status_icon} **{task['title']}** [{task['priority']}]{deadline_str}\n"
        if task['description']:
            result += f"   {task['description']}\n"
        result += f"   Category: {task['category']} | ID: {task['id']}\n\n"
    
    return result


def complete_task(task_id: str) -> str:
    """
    Mark a task as completed.
    
    Args:
        task_id: The task ID to complete
    
    Returns:
        Confirmation message
    """
    if task_id not in TASKS_STORE:
        return f"❌ Task not found: {task_id}"
    
    TASKS_STORE[task_id]["status"] = "completed"
    TASKS_STORE[task_id]["completed_at"] = datetime.now().isoformat()
    
    return f"✓ Task completed: '{TASKS_STORE[task_id]['title']}'"


def update_task_priority(task_id: str, new_priority: str) -> str:
    """
    Update the priority of an existing task.
    
    Args:
        task_id: The task ID to update
        new_priority: New priority level (low, medium, high, urgent)
    
    Returns:
        Confirmation message
    """
    if task_id not in TASKS_STORE:
        return f"❌ Task not found: {task_id}"
    
    old_priority = TASKS_STORE[task_id]["priority"]
    TASKS_STORE[task_id]["priority"] = new_priority
    
    return f"✓ Task priority updated: '{TASKS_STORE[task_id]['title']}' ({old_priority} → {new_priority})"


def delete_task(task_id: str) -> str:
    """
    Delete a task.
    
    Args:
        task_id: The task ID to delete
    
    Returns:
        Confirmation message
    """
    if task_id not in TASKS_STORE:
        return f"❌ Task not found: {task_id}"
    
    task_title = TASKS_STORE[task_id]["title"]
    del TASKS_STORE[task_id]
    
    return f"✓ Task deleted: '{task_title}'"


def get_urgent_tasks() -> str:
    """
    Get all high priority and urgent tasks.
    
    Returns:
        List of urgent tasks
    """
    urgent_tasks = [
        t for t in TASKS_STORE.values() 
        if t["priority"] in ["high", "urgent"] and t["status"] == "pending"
    ]
    
    if not urgent_tasks:
        return "No urgent tasks at the moment. Great job! 🎉"
    
    result = f"**⚠️ {len(urgent_tasks)} Urgent Task(s):**\n\n"
    for task in urgent_tasks:
        deadline_str = f" | Due: {task['deadline']}" if task['deadline'] else ""
        result += f"🔴 **{task['title']}** [{task['priority']}]{deadline_str}\n"
        result += f"   Category: {task['category']}\n\n"
    
    return result
