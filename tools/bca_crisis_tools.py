"""BCA-specific crisis and catch-up planning tools.

These tools are designed for students who are behind on classes
and labs, juggling home duties, and feeling stressed. They
produce small, realistic micro-plans that can survive
interruptions, and log structured information to Memori using
Toon-based schemas.
"""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from schemas.toon_models import Task, ScheduleBlock, CrisisEpisode
from memory.memory_manager import (
    store_task,
    store_schedule_block,
    store_crisis_episode,
)


def plan_bca_catchup(
    days_missed: int,
    labs_missed: int,
    assignments_pending: int,
    upcoming_exam_in_days: Optional[int] = None,
    stress_level: Optional[str] = None,
    location: Optional[str] = None,
    available_hours: float = 2.0,
) -> str:
    """Plan a short, realistic BCA catch-up plan.

    This is meant to be called in "crisis" situations like:
    - 5+ days behind on classes
    - multiple pending assignments
    - upcoming exams with little prep

    The function:
    1. Assesses crisis severity.
    2. Logs a CrisisEpisode in Memori (coordinator context).
    3. Creates a few micro-tasks and one or two schedule blocks
       in the study context, stored as Toon-encoded structures.
    4. Returns a human-friendly summary of the next steps.
    """

    # -------------------------
    # 1) Assess severity
    # -------------------------
    if days_missed >= 6 or (upcoming_exam_in_days is not None and upcoming_exam_in_days <= 2):
        severity = "severe"
    elif days_missed >= 3 or assignments_pending >= 2 or labs_missed >= 1:
        severity = "moderate"
    else:
        severity = "mild"

    episode = CrisisEpisode(
        severity=severity,
        days_missed=days_missed,
        labs_missed=labs_missed,
        assignments_pending=assignments_pending,
        upcoming_exam_in_days=upcoming_exam_in_days,
        stress_level=stress_level,
        notes=f"location={location!r}, available_hours={available_hours}",
    )
    store_crisis_episode("coordinator", episode)

    # -------------------------
    # 2) Build micro-tasks (no more than 3–5)
    # -------------------------
    now_str = datetime.now().isoformat(timespec="minutes")
    task_id_prefix = now_str.replace(":", "-")

    tasks: List[Task] = []

    # Always start with very small, low-resistance steps.
    tasks.append(
        Task(
            id=f"{task_id_prefix}-notes",
            title="Message 1–2 classmates and ask for notes of missed classes",
            kind="notes",
            duration_estimate_min=10,
            location=location,
            energy_level="low",
        )
    )

    # Assignment-focused task, if relevant.
    if assignments_pending > 0:
        tasks.append(
            Task(
                id=f"{task_id_prefix}-assignments-overview",
                title="List all pending assignments with deadlines in one place",
                kind="assignment",
                duration_estimate_min=20,
                location=location,
                energy_level="medium",
            )
        )

    # Lab-focused task when labs are missed.
    if labs_missed > 0:
        tasks.append(
            Task(
                id=f"{task_id_prefix}-lab-plan",
                title="Ask lab partner / class group what was covered in missed labs",
                kind="lab",
                duration_estimate_min=15,
                location=location,
                energy_level="low",
            )
        )

    # Exam prep micro-task if an exam is near.
    if upcoming_exam_in_days is not None and upcoming_exam_in_days <= 7:
        tasks.append(
            Task(
                id=f"{task_id_prefix}-exam-outline",
                title="Write a 5–10 bullet outline of topics for the nearest exam",
                kind="exam_prep",
                duration_estimate_min=25,
                location=location,
                energy_level="medium",
            )
        )

    # Cap total tasks so plan feels doable.
    tasks = tasks[:5]

    # Store tasks in the study context.
    for t in tasks:
        store_task("study", t)

    # -------------------------
    # 3) Build one or two schedule blocks
    # -------------------------
    total_minutes = int(available_hours * 60)
    if total_minutes <= 0:
        total_minutes = 30

    # Split time into at most two blocks: focus + buffer.
    block_duration = min(90, total_minutes - 15) if total_minutes > 60 else total_minutes

    primary_block = ScheduleBlock(
        label="crisis_catchup_block_1",
        tasks=tasks,
        duration_min=block_duration,
        location=location or "home",
        explanation=(
            "Focus on tiny wins: get notes, list assignments, "
            "and understand what you missed before deep study."
        ),
    )
    store_schedule_block("study", primary_block)

    # -------------------------
    # 4) Human summary
    # -------------------------
    human_location = location or "wherever you are right now"
    summary_lines = [
        f"Crisis level: {severity.upper()} (days missed={days_missed}, labs missed={labs_missed}, "
        f"assignments pending={assignments_pending}, upcoming exam in days={upcoming_exam_in_days})",
        "",
        "Next ~" f"{block_duration} minutes at {human_location}:",
    ]

    for idx, t in enumerate(tasks, start=1):
        est = f" (~{t.duration_estimate_min} min)" if t.duration_estimate_min else ""
        summary_lines.append(f"{idx}. {t.title}{est}")

    summary_lines.append(
        "\nRemember: small wins count. Even completing the first 1–2 tasks is progress."  # noqa: E501
    )

    return "\n".join(summary_lines)


# ---------------------------------------------------------------------------
# Natural-language wrapper
# ---------------------------------------------------------------------------


def _infer_crisis_params_from_message(message: str) -> dict:
    """Heuristically infer crisis parameters from a free-form message.

    This is intentionally simple and conservative. It looks for
    a few key patterns and otherwise falls back to safe defaults
    tuned for a "5+ days behind" student crisis.
    """

    text = message.lower()

    # Defaults tuned for a "bad but not catastrophic" situation.
    days_missed = 5
    labs_missed = 0
    assignments_pending = 1
    upcoming_exam_in_days: Optional[int] = None
    stress_level = "high" if any(k in text for k in ["stressed", "overwhelmed", "panic", "anxious"]) else "medium"

    import re

    # Look for patterns like "missed 5 classes" or "5 days behind".
    for m in re.finditer(r"(\d+)\s+(day|days)", text):
        num = int(m.group(1))
        span = m.span()
        window = text[max(0, span[0] - 20) : span[1] + 20]
        if any(k in window for k in ["behind", "missed", "absent"]):
            days_missed = num
            break

    # Look for labs missed: "missed 2 labs" or "2 lab practicals".
    for m in re.finditer(r"(\d+)\s+(lab|labs|practical|practicals)", text):
        labs_missed = int(m.group(1))
        break

    # Look for assignments: "3 assignments" or "2 pending assignments".
    for m in re.finditer(r"(\d+)\s+(assignment|assignments|hw|homework)", text):
        assignments_pending = int(m.group(1))
        break

    # Look for exam timing: "exam in 3 days".
    exam_match = re.search(r"exam[^\d]*(in\s+)?(\d+)\s+(day|days)", text)
    if exam_match:
        upcoming_exam_in_days = int(exam_match.group(2))

    return {
        "days_missed": days_missed,
        "labs_missed": labs_missed,
        "assignments_pending": assignments_pending,
        "upcoming_exam_in_days": upcoming_exam_in_days,
        "stress_level": stress_level,
    }


def handle_bca_crisis(message: str, location: Optional[str] = None, available_hours: float = 2.0) -> str:
    """End-to-end BCA crisis handler for free-form messages.

    This tool:
    1. Infers crisis parameters from natural language.
    2. Calls ``plan_bca_catchup`` with those parameters.
    3. Returns the human-readable micro-plan.

    It is designed to be exposed directly as an Agno tool so
    that the Coordinator or Scheduling agent can simply call
    ``handle_bca_crisis(message=...)`` when a crisis is detected.
    """

    params = _infer_crisis_params_from_message(message)
    return plan_bca_catchup(location=location, available_hours=available_hours, **params)
