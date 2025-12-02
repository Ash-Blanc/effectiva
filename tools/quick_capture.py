"""Quick capture tools for phone-based productivity.

This module provides simple, fast tools for students to capture
tasks, ideas, and notes quickly without complex interfaces.
Optimized for mobile usage patterns.
"""
from datetime import datetime
from typing import Optional, Dict, Any
import re

# Simple in-memory storage for quick captures
QUICK_CAPTURES = []

def quick_add_task(description: str, priority: str = "medium", due_date: Optional[str] = None) -> str:
    """
    Quickly add a task with minimal input.

    Args:
        description: Task description (can be natural language)
        priority: 'high', 'medium', 'low' (defaults to medium)
        due_date: Optional due date in YYYY-MM-DD format

    Returns:
        Confirmation message
    """
    task_id = f"quick_{len(QUICK_CAPTURES) + 1}_{datetime.now().timestamp()}"

    # Parse natural language priority if not specified
    if priority == "medium":  # Check for priority keywords in description
        desc_lower = description.lower()
        if any(word in desc_lower for word in ['urgent', 'asap', 'important', 'critical']):
            priority = 'high'
        elif any(word in desc_lower for word in ['low', 'sometime', 'eventually']):
            priority = 'low'

    task = {
        'id': task_id,
        'type': 'task',
        'description': description,
        'priority': priority,
        'due_date': due_date,
        'created_at': datetime.now().isoformat(),
        'status': 'pending'
    }

    QUICK_CAPTURES.append(task)

    priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '🟡')
    return f"{priority_emoji} Task captured: '{description}'"

def quick_note(content: str, category: str = "general") -> str:
    """
    Quickly capture a note or idea.

    Args:
        content: Note content
        category: 'study', 'work', 'personal', 'idea', 'general'

    Returns:
        Confirmation message
    """
    note_id = f"note_{len(QUICK_CAPTURES) + 1}_{datetime.now().timestamp()}"

    note = {
        'id': note_id,
        'type': 'note',
        'content': content,
        'category': category,
        'created_at': datetime.now().isoformat()
    }

    QUICK_CAPTURES.append(note)

    category_emoji = {
        'study': '📚', 'work': '💼', 'personal': '🏠',
        'idea': '💡', 'general': '📝'
    }.get(category, '📝')

    return f"{category_emoji} Note captured: '{content[:50]}...'"

def quick_reminder(message: str, when: Optional[str] = None) -> str:
    """
    Quickly set a reminder.

    Args:
        message: Reminder message
        when: When to remind (e.g., "tomorrow 2pm", "in 1 hour")

    Returns:
        Confirmation message
    """
    reminder_id = f"reminder_{len(QUICK_CAPTURES) + 1}_{datetime.now().timestamp()}"

    reminder = {
        'id': reminder_id,
        'type': 'reminder',
        'message': message,
        'when': when or "asap",
        'created_at': datetime.now().isoformat(),
        'status': 'pending'
    }

    QUICK_CAPTURES.append(reminder)

    return f"⏰ Reminder set: '{message}' ({when or 'ASAP'})"

def quick_energy_check(mood: str = "unknown", energy_level: str = "medium") -> str:
    """
    Quick energy and mood check for scheduling optimization.

    Args:
        mood: Current mood ('great', 'good', 'okay', 'tired', 'stressed')
        energy_level: Energy level ('high', 'medium', 'low')

    Returns:
        Confirmation and scheduling suggestion
    """
    check_id = f"energy_{len(QUICK_CAPTURES) + 1}_{datetime.now().timestamp()}"

    check = {
        'id': check_id,
        'type': 'energy_check',
        'mood': mood,
        'energy_level': energy_level,
        'timestamp': datetime.now().isoformat()
    }

    QUICK_CAPTURES.append(check)

    # Provide immediate scheduling advice based on energy
    if energy_level == "high":
        advice = "Great energy! Schedule deep work or challenging tasks now."
    elif energy_level == "medium":
        advice = "Good energy for regular tasks. Take short breaks every 45 minutes."
    else:  # low
        advice = "Low energy detected. Schedule light tasks or rest. Consider a short walk."

    mood_emoji = {
        'great': '😊', 'good': '🙂', 'okay': '😐',
        'tired': '😴', 'stressed': '😰'
    }.get(mood, '🤔')

    return f"{mood_emoji} Energy check logged. {advice}"

def get_recent_captures(limit: int = 5) -> str:
    """
    Get recent quick captures for review.

    Args:
        limit: Number of recent captures to show

    Returns:
        Formatted list of recent captures
    """
    recent = QUICK_CAPTURES[-limit:] if QUICK_CAPTURES else []

    if not recent:
        return "No recent captures found. Start capturing tasks, notes, and reminders!"

    result = f"**Recent Quick Captures (last {len(recent)}):**\n\n"

    for item in recent:
        timestamp = datetime.fromisoformat(item['created_at']).strftime('%m/%d %H:%M')

        if item['type'] == 'task':
            priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(item['priority'], '🟡')
            result += f"{priority_emoji} TASK: {item['description']} ({timestamp})\n"
        elif item['type'] == 'note':
            category_emoji = {
                'study': '📚', 'work': '💼', 'personal': '🏠',
                'idea': '💡', 'general': '📝'
            }.get(item['category'], '📝')
            result += f"{category_emoji} NOTE: {item['content'][:60]}... ({timestamp})\n"
        elif item['type'] == 'reminder':
            result += f"⏰ REMINDER: {item['message']} ({item['when']}) - {timestamp}\n"
        elif item['type'] == 'energy_check':
            mood_emoji = {
                'great': '😊', 'good': '🙂', 'okay': '😐',
                'tired': '😴', 'stressed': '😰'
            }.get(item['mood'], '🤔')
            result += f"{mood_emoji} ENERGY: {item['energy_level']} energy ({timestamp})\n"

    result += f"\n**Total captures:** {len(QUICK_CAPTURES)}"
    return result

def process_natural_capture(text: str) -> str:
    """
    Process natural language capture and route to appropriate tool.

    Examples:
    - "remind me to study calculus tomorrow at 2pm"
    - "task: finish lab report by friday high priority"
    - "note: great idea for project - use machine learning"
    - "feeling tired today"

    Args:
        text: Natural language input

    Returns:
        Processing result
    """
    text_lower = text.lower().strip()

    # Task detection
    if any(word in text_lower for word in ['task:', 'todo:', 'do:', 'need to']):
        # Extract task description
        task_text = re.sub(r'^(task|todo|do):\s*', '', text, flags=re.IGNORECASE)
        # Check for priority keywords
        priority = 'medium'
        if any(word in task_text.lower() for word in ['urgent', 'asap', 'important']):
            priority = 'high'
        elif any(word in task_text.lower() for word in ['low', 'sometime']):
            priority = 'low'
        return quick_add_task(task_text.strip(), priority)

    # Reminder detection
    elif any(word in text_lower for word in ['remind', 'reminder', 'remind me']):
        return quick_reminder(text)

    # Note detection
    elif any(word in text_lower for word in ['note:', 'idea:', 'remember:']):
        category = 'general'
        if 'study' in text_lower:
            category = 'study'
        elif 'work' in text_lower or 'job' in text_lower:
            category = 'work'
        elif 'personal' in text_lower:
            category = 'personal'
        note_text = re.sub(r'^(note|idea|remember):\s*', '', text, flags=re.IGNORECASE)
        return quick_note(note_text.strip(), category)

    # Energy/mood detection
    elif any(word in text_lower for word in ['feeling', 'feel', 'energy', 'mood', 'tired', 'great', 'good', 'stressed']):
        mood = 'unknown'
        energy = 'medium'

        if any(word in text_lower for word in ['tired', 'exhausted', 'drained']):
            mood = 'tired'
            energy = 'low'
        elif any(word in text_lower for word in ['great', 'awesome', 'energized']):
            mood = 'great'
            energy = 'high'
        elif any(word in text_lower for word in ['good', 'okay', 'fine']):
            mood = 'good'
            energy = 'medium'
        elif any(word in text_lower for word in ['stressed', 'anxious', 'overwhelmed']):
            mood = 'stressed'
            energy = 'low'

        return quick_energy_check(mood, energy)

    # Default to note
    else:
        return quick_note(text)