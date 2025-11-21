"""Time management and scheduling optimization tools."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json


def create_time_block(
    activity: str,
    duration_minutes: int,
    preferred_time: Optional[str] = None,
    priority: str = "medium"
) -> str:
    """
    Create a time block for a specific activity.
    
    Args:
        activity: Activity description
        duration_minutes: Duration in minutes
        preferred_time: Preferred start time (HH:MM format)
        priority: Priority level
    
    Returns:
        Time block suggestion
    """
    if preferred_time:
        result = f"⏰ Time Block Created:\n"
        result += f"**Activity:** {activity}\n"
        result += f"**Duration:** {duration_minutes} minutes\n"
        result += f"**Suggested Time:** {preferred_time}\n"
        result += f"**Priority:** {priority}\n"
    else:
        # Suggest time based on priority
        time_suggestions = {
            "urgent": "As soon as possible",
            "high": "Within the next 2 hours",
            "medium": "Today, during a free slot",
            "low": "When convenient, this week"
        }
        
        result = f"⏰ Time Block Created:\n"
        result += f"**Activity:** {activity}\n"
        result += f"**Duration:** {duration_minutes} minutes\n"
        result += f"**Recommendation:** {time_suggestions.get(priority, 'Schedule when convenient')}\n"
    
    return result


def suggest_study_schedule(
    subjects: List[str],
    total_study_hours: int = 4,
    break_duration: int = 15
) -> str:
    """
    Generate an optimal study schedule using time-blocking.
    
    Args:
        subjects: List of subjects to study
        total_study_hours: Total hours available for studying
        break_duration: Break duration in minutes between sessions
    
    Returns:
        Suggested study schedule
    """
    if not subjects:
        return "❌ Please provide at least one subject to study."
    
    total_minutes = total_study_hours * 60
    num_subjects = len(subjects)
    
    # Pomodoro-style: 50 min study, 15 min break
    session_duration = 50
    num_sessions = total_minutes // (session_duration + break_duration)
    
    # Distribute sessions across subjects
    sessions_per_subject = max(1, num_sessions // num_subjects)
    
    result = f"**📚 Study Schedule ({total_study_hours}h total):**\n\n"
    result += f"Using Pomodoro technique: {session_duration} min study + {break_duration} min break\n\n"
    
    current_time = datetime.now()
    session_num = 1
    
    for subject in subjects:
        for _ in range(sessions_per_subject):
            start = current_time.strftime("%H:%M")
            current_time += timedelta(minutes=session_duration)
            end = current_time.strftime("%H:%M")
            
            result += f"**Session {session_num}:** {start}-{end} - {subject}\n"
            
            # Add break
            if session_num < num_sessions:
                current_time += timedelta(minutes=break_duration)
                result += f"   ☕ Break: {break_duration} min\n"
            
            session_num += 1
    
    return result


def calculate_time_needed(
    tasks: List[Dict[str, any]],
    include_breaks: bool = True
) -> str:
    """
    Calculate total time needed for a list of tasks.
    
    Args:
        tasks: List of task dictionaries with 'name' and 'duration_minutes'
        include_breaks: Whether to include break time
    
    Returns:
        Time calculation summary
    """
    if not tasks:
        return "No tasks provided."
    
    total_minutes = sum(task.get("duration_minutes", 30) for task in tasks)
    
    if include_breaks:
        # Add 10 min break between tasks
        break_time = (len(tasks) - 1) * 10
        total_minutes += break_time
    
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    result = f"**⏱️ Time Calculation:**\n\n"
    result += f"**Number of tasks:** {len(tasks)}\n"
    result += f"**Total time needed:** {hours}h {minutes}m\n\n"
    
    result += "**Task Breakdown:**\n"
    for i, task in enumerate(tasks, 1):
        name = task.get("name", f"Task {i}")
        duration = task.get("duration_minutes", 30)
        result += f"{i}. {name}: {duration} min\n"
    
    if include_breaks:
        result += f"\n*Includes {break_time} minutes of break time*"
    
    return result


def prioritize_tasks_by_deadline(tasks_with_deadlines: List[Dict]) -> str:
    """
    Prioritize tasks based on deadlines and importance.
    
    Args:
        tasks_with_deadlines: List of tasks with 'name', 'deadline', 'importance'
    
    Returns:
        Prioritized task list
    """
    if not tasks_with_deadlines:
        return "No tasks provided."
    
    today = datetime.now()
    
    # Calculate urgency score for each task
    for task in tasks_with_deadlines:
        deadline_str = task.get("deadline", "")
        if deadline_str:
            try:
                deadline = datetime.fromisoformat(deadline_str)
                days_until = (deadline - today).days
                task["urgency_score"] = max(0, 10 - days_until)
            except:
                task["urgency_score"] = 5
        else:
            task["urgency_score"] = 5
        
        # Combine urgency with importance
        importance_map = {"low": 1, "medium": 2, "high": 3, "urgent": 4}
        importance = task.get("importance", "medium")
        task["priority_score"] = task["urgency_score"] + importance_map.get(importance, 2) * 2
    
    # Sort by priority score (descending)
    sorted_tasks = sorted(tasks_with_deadlines, key=lambda x: x["priority_score"], reverse=True)
    
    result = "**📋 Prioritized Task List:**\n\n"
    
    for i, task in enumerate(sorted_tasks, 1):
        name = task.get("name", f"Task {i}")
        deadline = task.get("deadline", "No deadline")
        importance = task.get("importance", "medium")
        
        # Priority emoji
        if task["priority_score"] >= 10:
            emoji = "🔴"
        elif task["priority_score"] >= 7:
            emoji = "🟡"
        else:
            emoji = "🟢"
        
        result += f"{emoji} **{i}. {name}**\n"
        result += f"   Deadline: {deadline} | Importance: {importance}\n\n"
    
    return result


def suggest_break_schedule(work_duration_hours: int) -> str:
    """
    Suggest an optimal break schedule for the given work duration.
    
    Args:
        work_duration_hours: Hours of continuous work planned
    
    Returns:
        Break schedule suggestion
    """
    if work_duration_hours <= 0:
        return "❌ Work duration must be positive."
    
    result = f"**☕ Break Schedule for {work_duration_hours}h work session:**\n\n"
    
    # Pomodoro-inspired break schedule
    if work_duration_hours <= 2:
        result += "• Take a 5-10 minute break every 50 minutes\n"
        result += f"• Expected breaks: {work_duration_hours * 2} short breaks"
    else:
        result += "**Recommended schedule:**\n"
        result += "• 50 minutes work → 10 minute short break\n"
        result += "• After 4 sessions (≈3.3h) → 30 minute long break\n"
        result += f"• Total short breaks: {work_duration_hours * 2}\n"
        result += f"• Total long breaks: {max(0, (work_duration_hours // 4))}\n\n"
        result += "**Tips:**\n"
        result += "- Stand up and stretch during breaks\n"
        result += "- Stay hydrated\n"
        result += "- Step away from your workspace\n"
        result += "- Do light exercise or walk around"
    
    return result
