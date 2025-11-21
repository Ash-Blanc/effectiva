"""Context management tools for shapeshifting between study, work, and life modes."""
from typing import Dict, Optional
from datetime import datetime


# Current context state
CURRENT_CONTEXT = {
    "mode": "balanced",
    "last_updated": datetime.now().isoformat(),
    "focus_area": None,
    "preferences": {}
}

# Context history
CONTEXT_HISTORY = []


def switch_context(mode: str, focus_area: Optional[str] = None) -> str:
    """
    Switch to a different context mode (shapeshifting).
    
    Args:
        mode: The context mode to switch to (study, work, life, balanced)
        focus_area: Optional specific area within the mode
    
    Returns:
        Confirmation message with context details
    """
    valid_modes = ["study", "work", "life", "balanced"]
    
    if mode not in valid_modes:
        return f"❌ Invalid mode. Choose from: {', '.join(valid_modes)}"
    
    # Save previous context to history
    CONTEXT_HISTORY.append(CURRENT_CONTEXT.copy())
    
    # Update current context
    CURRENT_CONTEXT["mode"] = mode
    CURRENT_CONTEXT["focus_area"] = focus_area
    CURRENT_CONTEXT["last_updated"] = datetime.now().isoformat()
    
    # Mode-specific messages
    mode_messages = {
        "study": "📚 Switched to Study Mode. Let's focus on learning!",
        "work": "💼 Switched to Work Mode. Time to be productive!",
        "life": "🏠 Switched to Life Mode. Let's manage personal tasks!",
        "balanced": "⚖️ Switched to Balanced Mode. Managing all aspects together!"
    }
    
    message = mode_messages.get(mode, f"✓ Context switched to {mode}")
    
    if focus_area:
        message += f"\n🎯 Focus: {focus_area}"
    
    return message


def get_current_context() -> str:
    """
    Get the current context mode and details.
    
    Returns:
        Current context information
    """
    mode = CURRENT_CONTEXT["mode"]
    focus = CURRENT_CONTEXT.get("focus_area")
    last_updated = CURRENT_CONTEXT["last_updated"]
    
    # Mode emojis
    mode_emojis = {
        "study": "📚",
        "work": "💼",
        "life": "🏠",
        "balanced": "⚖️"
    }
    
    emoji = mode_emojis.get(mode, "")
    result = f"**Current Context:** {emoji} {mode.capitalize()} Mode\n"
    
    if focus:
        result += f"**Focus Area:** {focus}\n"
    
    result += f"**Last Updated:** {last_updated[:19]}"
    
    return result


def set_context_preference(key: str, value: str) -> str:
    """
    Set a preference for the current context.
    
    Args:
        key: Preference key (e.g., 'study_duration', 'break_frequency')
        value: Preference value
    
    Returns:
        Confirmation message
    """
    CURRENT_CONTEXT["preferences"][key] = value
    
    return f"✓ Preference set: {key} = {value} for {CURRENT_CONTEXT['mode']} mode"


def get_context_preferences() -> str:
    """
    Get all preferences for the current context.
    
    Returns:
        List of context preferences
    """
    preferences = CURRENT_CONTEXT.get("preferences", {})
    
    if not preferences:
        return f"No preferences set for {CURRENT_CONTEXT['mode']} mode."
    
    result = f"**Preferences for {CURRENT_CONTEXT['mode'].capitalize()} Mode:**\n\n"
    for key, value in preferences.items():
        result += f"• {key}: {value}\n"
    
    return result


def get_context_suggestions() -> str:
    """
    Get suggestions based on the current context mode.
    
    Returns:
        Context-specific suggestions
    """
    mode = CURRENT_CONTEXT["mode"]
    
    suggestions = {
        "study": [
            "Create focused study blocks using the Pomodoro technique",
            "Review your upcoming assignments and deadlines",
            "Organize your study materials and notes",
            "Set specific learning goals for today"
        ],
        "work": [
            "Check your work schedule and upcoming shifts",
            "Review job-related tasks and priorities",
            "Prepare for meetings or check-ins",
            "Update your professional development goals"
        ],
        "life": [
            "Review your household chores and responsibilities",
            "Check personal appointments and errands",
            "Plan meals and grocery shopping",
            "Schedule self-care and relaxation time"
        ],
        "balanced": [
            "Review tasks across all areas (study, work, life)",
            "Identify time conflicts and priorities",
            "Create a balanced daily schedule",
            "Check for urgent items in any area"
        ]
    }
    
    mode_suggestions = suggestions.get(mode, [])
    
    result = f"**Suggestions for {mode.capitalize()} Mode:**\n\n"
    for i, suggestion in enumerate(mode_suggestions, 1):
        result += f"{i}. {suggestion}\n"
    
    return result


def view_context_history(limit: int = 5) -> str:
    """
    View recent context switches.
    
    Args:
        limit: Number of recent switches to show
    
    Returns:
        Context switch history
    """
    if not CONTEXT_HISTORY:
        return "No context history yet."
    
    recent = CONTEXT_HISTORY[-limit:]
    
    result = f"**Recent Context Switches (last {len(recent)}):**\n\n"
    for i, ctx in enumerate(reversed(recent), 1):
        mode = ctx["mode"]
        time = ctx["last_updated"][:19]
        focus = ctx.get("focus_area", "")
        focus_str = f" ({focus})" if focus else ""
        result += f"{i}. {mode.capitalize()}{focus_str} - {time}\n"
    
    return result
