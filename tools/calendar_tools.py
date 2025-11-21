"""Calendar and event management tools for scheduling."""
from datetime import datetime, timedelta
from typing import Optional, List


# Simple in-memory calendar storage
EVENTS_STORE = {}


def add_event(
    title: str,
    start_time: str,
    end_time: str,
    category: str = "general",
    description: str = "",
    location: str = ""
) -> str:
    """
    Add a new event to the calendar.
    
    Args:
        title: Event title
        start_time: Start time in ISO format (YYYY-MM-DDTHH:MM)
        end_time: End time in ISO format (YYYY-MM-DDTHH:MM)
        category: Event category (class, work, study, personal, meeting)
        description: Event description
        location: Event location
    
    Returns:
        Confirmation message with event ID
    """
    event_id = f"event_{len(EVENTS_STORE) + 1}_{datetime.now().timestamp()}"
    
    event = {
        "id": event_id,
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "category": category,
        "description": description,
        "location": location,
        "created_at": datetime.now().isoformat()
    }
    
    EVENTS_STORE[event_id] = event
    
    return f"✓ Event added: '{title}' on {start_time[:10]} from {start_time[11:16]} to {end_time[11:16]}"


def get_events(date: Optional[str] = None, category: Optional[str] = None) -> str:
    """
    Get events, optionally filtered by date or category.
    
    Args:
        date: Filter by date (YYYY-MM-DD), defaults to today
        category: Filter by category
    
    Returns:
        Formatted list of events
    """
    if date is None:
        date = datetime.now().date().isoformat()
    
    events = list(EVENTS_STORE.values())
    
    # Filter by date
    events = [e for e in events if e["start_time"].startswith(date)]
    
    # Filter by category if specified
    if category:
        events = [e for e in events if e["category"] == category]
    
    if not events:
        return f"No events found for {date}."
    
    # Sort by start time
    events.sort(key=lambda e: e["start_time"])
    
    result = f"**Events for {date}:**\n\n"
    for event in events:
        start = event["start_time"][11:16]
        end = event["end_time"][11:16]
        result += f"📅 {start}-{end}: **{event['title']}** [{event['category']}]\n"
        if event["location"]:
            result += f"   📍 {event['location']}\n"
        if event["description"]:
            result += f"   {event['description']}\n"
        result += f"   ID: {event['id']}\n\n"
    
    return result


def find_free_slots(date: str, duration_minutes: int = 60) -> str:
    """
    Find free time slots on a given date.
    
    Args:
        date: Date to check (YYYY-MM-DD)
        duration_minutes: Minimum duration needed in minutes
    
    Returns:
        List of available time slots
    """
    # Get all events for the date
    events = [e for e in EVENTS_STORE.values() if e["start_time"].startswith(date)]
    
    if not events:
        return f"The entire day {date} is free!"
    
    # Sort events by start time
    events.sort(key=lambda e: e["start_time"])
    
    # Define working hours (8 AM to 10 PM)
    day_start = datetime.fromisoformat(f"{date}T08:00:00")
    day_end = datetime.fromisoformat(f"{date}T22:00:00")
    
    free_slots = []
    current_time = day_start
    
    for event in events:
        event_start = datetime.fromisoformat(event["start_time"])
        event_end = datetime.fromisoformat(event["end_time"])
        
        # Check if there's a gap before this event
        if (event_start - current_time).total_seconds() / 60 >= duration_minutes:
            free_slots.append(
                f"{current_time.strftime('%H:%M')} - {event_start.strftime('%H:%M')}"
            )
        
        current_time = max(current_time, event_end)
    
    # Check remaining time after last event
    if (day_end - current_time).total_seconds() / 60 >= duration_minutes:
        free_slots.append(
            f"{current_time.strftime('%H:%M')} - {day_end.strftime('%H:%M')}"
        )
    
    if not free_slots:
        return f"No free slots of {duration_minutes} minutes found on {date}."
    
    result = f"**Free time slots on {date} (min {duration_minutes} min):**\n\n"
    for slot in free_slots:
        result += f"🕐 {slot}\n"
    
    return result


def delete_event(event_id: str) -> str:
    """
    Delete an event from the calendar.
    
    Args:
        event_id: The event ID to delete
    
    Returns:
        Confirmation message
    """
    if event_id not in EVENTS_STORE:
        return f"❌ Event not found: {event_id}"
    
    event_title = EVENTS_STORE[event_id]["title"]
    del EVENTS_STORE[event_id]
    
    return f"✓ Event deleted: '{event_title}'"


def get_upcoming_events(days: int = 7) -> str:
    """
    Get all upcoming events for the next N days.
    
    Args:
        days: Number of days to look ahead
    
    Returns:
        List of upcoming events
    """
    today = datetime.now()
    end_date = today + timedelta(days=days)
    
    upcoming = [
        e for e in EVENTS_STORE.values()
        if today <= datetime.fromisoformat(e["start_time"]) <= end_date
    ]
    
    if not upcoming:
        return f"No events scheduled for the next {days} days."
    
    # Sort by start time
    upcoming.sort(key=lambda e: e["start_time"])
    
    result = f"**Upcoming Events (next {days} days):**\n\n"
    for event in upcoming:
        date = event["start_time"][:10]
        start = event["start_time"][11:16]
        result += f"📅 {date} at {start}: **{event['title']}** [{event['category']}]\n"
    
    return result
