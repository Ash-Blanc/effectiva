"""Time management and scheduling optimization tools with energy awareness."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from tools.quick_capture import QUICK_CAPTURES
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


def get_current_energy_level() -> str:
    """
    Get the most recent energy level from quick captures.

    Returns:
        Current energy level ('high', 'medium', 'low', or 'unknown')
    """
    # Get recent energy checks from quick captures
    energy_checks = [item for item in QUICK_CAPTURES
                    if item.get('type') == 'energy_check']

    if not energy_checks:
        return 'unknown'

    # Get the most recent energy check
    latest_check = max(energy_checks, key=lambda x: x.get('timestamp', ''))
    return latest_check.get('energy_level', 'medium')


def suggest_optimal_time_for_task(task_type: str, duration_minutes: int = 60) -> str:
    """
    Suggest the optimal time for a task based on energy levels and task type.

    Args:
        task_type: Type of task ('study', 'creative', 'analytical', 'physical', 'meeting')
        duration_minutes: Task duration in minutes

    Returns:
        Time suggestion with reasoning
    """
    current_energy = get_current_energy_level()
    current_hour = datetime.now().hour

    # Energy-based time recommendations
    energy_recommendations = {
        'high': {
            'best_times': ['8:00-12:00', '14:00-16:00'],
            'reason': 'High energy - tackle challenging tasks during peak focus times'
        },
        'medium': {
            'best_times': ['9:00-11:00', '15:00-17:00'],
            'reason': 'Medium energy - schedule regular tasks during moderate focus periods'
        },
        'low': {
            'best_times': ['10:00-12:00', '16:00-18:00'],
            'reason': 'Low energy - focus on lighter tasks during easier periods'
        },
        'unknown': {
            'best_times': ['9:00-11:00', '14:00-16:00'],
            'reason': 'Default schedule - adjust based on your energy patterns'
        }
    }

    # Task-specific time preferences
    task_preferences = {
        'study': {
            'optimal_times': ['8:00-12:00', '19:00-21:00'],
            'reason': 'Morning for deep focus, evening for review'
        },
        'creative': {
            'optimal_times': ['10:00-12:00', '20:00-22:00'],
            'reason': 'Mid-morning when mind is flexible, evening when relaxed'
        },
        'analytical': {
            'optimal_times': ['9:00-11:00', '14:00-16:00'],
            'reason': 'Morning analytical peak, early afternoon focus'
        },
        'physical': {
            'optimal_times': ['7:00-9:00', '17:00-19:00'],
            'reason': 'Morning energy boost, evening stress relief'
        },
        'meeting': {
            'optimal_times': ['9:00-11:00', '14:00-16:00'],
            'reason': 'Standard business hours for coordination'
        }
    }

    energy_rec = energy_recommendations.get(current_energy, energy_recommendations['unknown'])
    task_rec = task_preferences.get(task_type, task_preferences.get('study', {}))

    result = f"**🎯 Optimal Time for {task_type.title()} Task ({duration_minutes}min):**\n\n"

    # Current energy status
    energy_emoji = {'high': '⚡', 'medium': '🔋', 'low': '🪫', 'unknown': '❓'}.get(current_energy, '❓')
    result += f"**Current Energy:** {energy_emoji} {current_energy.title()}\n\n"

    # Energy-based recommendation
    result += f"**Energy-Based Suggestion:**\n{energy_rec['reason']}\n"
    result += f"**Recommended Times:** {', '.join(energy_rec['best_times'])}\n\n"

    # Task-specific recommendation
    result += f"**Task-Specific Guidance:**\n{task_rec['reason']}\n"
    result += f"**Optimal Times:** {', '.join(task_rec['optimal_times'])}\n\n"

    # Immediate suggestion based on current time
    now = datetime.now()
    current_time_str = now.strftime('%H:%M')

    # Find next available optimal slot
    next_slot = find_next_optimal_slot(task_type, current_energy, duration_minutes)

    if next_slot:
        result += f"**Next Available Slot:** {next_slot}\n"
    else:
        result += f"**Current Time ({current_time_str}):** Check if this works for your energy level\n"

    return result


def find_next_optimal_slot(task_type: str, energy_level: str, duration_minutes: int) -> Optional[str]:
    """
    Find the next optimal time slot for a task.

    Args:
        task_type: Type of task
        energy_level: Current energy level
        duration_minutes: Task duration

    Returns:
        Next optimal time slot or None
    """
    now = datetime.now()
    current_hour = now.hour

    # Define optimal time ranges based on task type and energy
    optimal_ranges = {
        ('study', 'high'): [(8, 12), (19, 21)],
        ('study', 'medium'): [(9, 11), (15, 17)],
        ('study', 'low'): [(10, 12), (16, 18)],
        ('creative', 'high'): [(10, 12), (20, 22)],
        ('creative', 'medium'): [(14, 16), (19, 21)],
        ('analytical', 'high'): [(9, 11), (14, 16)],
        ('meeting', 'any'): [(9, 11), (14, 16)],
    }

    # Get ranges for this task/energy combination
    ranges = optimal_ranges.get((task_type, energy_level)) or optimal_ranges.get((task_type, 'any')) or [(9, 17)]

    # Find next available slot today
    for start_hour, end_hour in ranges:
        if current_hour < start_hour:
            # Slot is later today
            slot_start = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
            slot_end = slot_start + timedelta(minutes=duration_minutes)
            if slot_end.hour <= end_hour:
                return f"Today {slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"

    # If no slots today, suggest tomorrow morning
    tomorrow = now + timedelta(days=1)
    return f"Tomorrow {ranges[0][0]:02d}:00-{(ranges[0][0] + duration_minutes//60):02d}:{duration_minutes%60:02d}"


def create_energy_aware_schedule(tasks: List[Dict], available_hours: int = 8) -> str:
    """
    Create a schedule that considers energy levels and task difficulty.

    Args:
        tasks: List of tasks with 'name', 'difficulty', 'duration_minutes'
        available_hours: Total hours available for work

    Returns:
        Energy-aware schedule
    """
    if not tasks:
        return "No tasks provided for scheduling."

    current_energy = get_current_energy_level()
    total_minutes = available_hours * 60

    # Sort tasks by energy requirements
    energy_task_order = {
        'high': ['easy', 'medium', 'hard'],  # Start easy when energy is high
        'medium': ['medium', 'easy', 'hard'],  # Mix when energy is medium
        'low': ['easy', 'medium'],  # Only easy/medium when energy is low
        'unknown': ['easy', 'medium', 'hard']  # Default ordering
    }

    preferred_order = energy_task_order.get(current_energy, energy_task_order['unknown'])

    # Sort tasks according to energy-aware ordering
    def task_sort_key(task):
        difficulty = task.get('difficulty', 'medium')
        try:
            return preferred_order.index(difficulty)
        except ValueError:
            return len(preferred_order)  # Put unknown difficulties at end

    sorted_tasks = sorted(tasks, key=task_sort_key)

    result = f"**⚡ Energy-Aware Schedule ({available_hours}h available):**\n\n"
    result += f"**Current Energy Level:** {current_energy.title()}\n\n"

    # Schedule explanation
    if current_energy == 'high':
        result += "💪 **High Energy Plan:** Start with challenging tasks, maintain momentum\n\n"
    elif current_energy == 'medium':
        result += "🔋 **Medium Energy Plan:** Balance difficulty, include breaks\n\n"
    elif current_energy == 'low':
        result += "🪫 **Low Energy Plan:** Focus on easier tasks, shorter sessions\n\n"
    else:
        result += "🤔 **Default Plan:** Balanced approach for unknown energy\n\n"

    current_time = datetime.now()
    scheduled_minutes = 0

    for i, task in enumerate(sorted_tasks, 1):
        task_duration = task.get('duration_minutes', 30)
        task_name = task.get('name', f'Task {i}')
        difficulty = task.get('difficulty', 'medium')

        if scheduled_minutes + task_duration > total_minutes:
            break

        # Format time slot
        start_time = current_time.strftime('%H:%M')
        current_time += timedelta(minutes=task_duration)
        end_time = current_time.strftime('%H:%M')

        # Difficulty emoji
        diff_emoji = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}.get(difficulty, '🤔')

        result += f"**{i}. {diff_emoji} {task_name}**\n"
        result += f"   ⏰ {start_time}-{end_time} ({task_duration}min)\n"
        result += f"   📊 Difficulty: {difficulty}\n\n"

        scheduled_minutes += task_duration

        # Add breaks for medium/low energy
        if current_energy in ['medium', 'low'] and i < len(sorted_tasks):
            break_duration = 10 if current_energy == 'medium' else 15
            current_time += timedelta(minutes=break_duration)
            result += f"   ☕ Break: {break_duration} minutes\n\n"
            scheduled_minutes += break_duration

    remaining_minutes = total_minutes - scheduled_minutes
    if remaining_minutes > 0:
        result += f"**💡 Remaining time:** {remaining_minutes} minutes\n"
        result += "Use for review, planning, or flexible tasks."

    return result
