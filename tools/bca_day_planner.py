"""BCA normal-day planning tools.

These tools help plan a realistic, interruption-aware day for
BCA students, taking into account whether they are at home or
college and what kinds of work are currently important
(assignments, labs, projects, exams, practice).

They create Toon-encoded ScheduleBlocks (and sometimes Tasks)
stored via Memori, and return a human-readable summary that the
agents can present to the user.
"""
from __future__ import annotations

from typing import List, Optional

from schemas.toon_models import Task, ScheduleBlock
from memory.memory_manager import store_task, store_schedule_block


def plan_bca_day(
    location: str = "home",
    available_hours: float = 6.0,
    assignments_pending: int = 0,
    labs_today: int = 0,
    projects_active: bool = False,
    upcoming_exam_in_days: Optional[int] = None,
) -> str:
    """Plan a typical BCA student's day.

    Args:
        location: "home" or "college" (other values are treated like "home").
        available_hours: Rough total hours the student can dedicate today.
        assignments_pending: Count of pending assignments.
        labs_today: Number of lab sessions or lab-related tasks today.
        projects_active: Whether there is an active project that needs work.
        upcoming_exam_in_days: Days until the nearest important exam, if known.

    Returns:
        A human-readable description of the planned day.
    """

    loc = (location or "home").lower()
    if loc not in {"home", "college"}:
        loc = "home"

    total_min = max(90, int(available_hours * 60))  # at least 1.5 hours

    # We will create up to 3 blocks: morning, afternoon, evening.
    # Each block gets a share of the total minutes.
    num_blocks = 3 if total_min >= 240 else 2 if total_min >= 150 else 1
    block_min = total_min // num_blocks

    tasks: List[Task] = []
    blocks: List[ScheduleBlock] = []

    # -------------------------
    # 1) Define task themes by location
    # -------------------------
    def add_task(title: str, kind: str, est: int, energy: str = "medium") -> Task:
        t = Task(
            id=f"bca-day-{kind}-{len(tasks)+1}",
            title=title,
            kind=kind,
            duration_estimate_min=est,
            location=loc,
            energy_level=energy,
        )
        tasks.append(t)
        store_task("study", t)
        return t

    # Morning / first block: heavier cognitive work
    morning_tasks: List[Task] = []
    if loc == "college":
        morning_tasks.append(
            add_task(
                "Attend / review today's core classes and take concise notes",
                kind="notes",
                est=block_min // 2,
                energy="high",
            )
        )
        if labs_today > 0:
            morning_tasks.append(
                add_task(
                    "Prepare questions or code snippets for today's lab sessions",
                    kind="lab_prep",
                    est=block_min // 3,
                )
            )
    else:  # home
        if assignments_pending > 0:
            morning_tasks.append(
                add_task(
                    "Work on the most urgent assignment (core theory or coding)",
                    kind="assignment",
                    est=block_min // 2,
                    energy="high",
                )
            )
        if upcoming_exam_in_days is not None and upcoming_exam_in_days <= 10:
            morning_tasks.append(
                add_task(
                    "Deep study: revise key topics for the nearest exam",
                    kind="exam_prep",
                    est=block_min // 3,
                    energy="high",
                )
            )

    if not morning_tasks:
        morning_tasks.append(
            add_task(
                "Focused study on the hardest subject right now",
                kind="study",
                est=block_min // 2,
                energy="high",
            )
        )

    blocks.append(
        ScheduleBlock(
            label="morning_block" if num_blocks > 1 else "main_block",
            tasks=morning_tasks,
            duration_min=block_min,
            location=loc,
            explanation=(
                "Start the day with your highest-impact work: classes/labs if at college, "
                "or urgent assignments/exam prep if at home."
            ),
        )
    )

    # Afternoon block: assignments / projects / labs catch-up
    if num_blocks >= 2:
        afternoon_tasks: List[Task] = []
        if assignments_pending > 1:
            afternoon_tasks.append(
                add_task(
                    "Continue or start the second most urgent assignment",
                    kind="assignment",
                    est=block_min // 2,
                )
            )
        if projects_active:
            afternoon_tasks.append(
                add_task(
                    "Project progress: implement or debug one small feature",
                    kind="project",
                    est=block_min // 3,
                )
            )
        if not afternoon_tasks:
            afternoon_tasks.append(
                add_task(
                    "Organize notes and consolidate what you studied earlier",
                    kind="notes",
                    est=block_min // 2,
                )
            )

        blocks.append(
            ScheduleBlock(
                label="afternoon_block",
                tasks=afternoon_tasks,
                duration_min=block_min,
                location=loc,
                explanation=(
                    "Use the afternoon for steady progress on assignments and projects, "
                    "or for consolidating class material."
                ),
            )
        )

    # Evening block: lighter practice + review
    if num_blocks >= 3:
        evening_tasks: List[Task] = []
        evening_tasks.append(
            add_task(
                "Coding practice: 1–3 small problems (DSA or language of the semester)",
                kind="practice",
                est=block_min // 2,
                energy="medium",
            )
        )
        if upcoming_exam_in_days is not None and upcoming_exam_in_days <= 7:
            evening_tasks.append(
                add_task(
                    "Light revision: flashcards or quick recap of today's topics",
                    kind="revision",
                    est=block_min // 3,
                    energy="low",
                )
            )

        blocks.append(
            ScheduleBlock(
                label="evening_block",
                tasks=evening_tasks,
                duration_min=block_min,
                location=loc,
                explanation=(
                    "In the evening, do lighter coding practice and gentle revision so you "
                    "can wind down without wasting the time."
                ),
            )
        )

    # Persist blocks
    for b in blocks:
        store_schedule_block("study", b)

    # -------------------------
    # Human summary
    # -------------------------
    loc_human = "college" if loc == "college" else "home / your own space"
    lines: List[str] = []
    lines.append(
        f"Planned day for a BCA student at {loc_human} (~{total_min} minutes total, {num_blocks} block(s))."
    )
    lines.append("")

    for b in blocks:
        lines.append(f"Block: {b.label.replace('_', ' ').title()} (~{b.duration_min} min)")
        for i, t in enumerate(b.tasks, start=1):
            est = f" (~{t.duration_estimate_min} min)" if t.duration_estimate_min else ""
            lines.append(f"  {i}. {t.title}{est}")
        lines.append("")

    lines.append(
        "Tip: it's okay if reality shifts—treat these blocks as anchors, "
        "not a rigid timetable."
    )

    return "\n".join(lines)


def handle_bca_day(message: str, default_location: Optional[str] = None) -> str:
    """Natural-language wrapper for normal BCA day planning.

    This parses a free-form message to infer location (home vs college),
    available hours, and rough workload signals, then calls ``plan_bca_day``.
    """

    text = message.lower()

    # Location
    if "college" in text or "campus" in text or "class" in text:
        location = "college"
    elif "home" in text or "house" in text:
        location = "home"
    else:
        location = default_location or "home"

    # Available hours (very simple heuristic: look for "X hours")
    import re

    available_hours = 6.0
    m = re.search(r"(\d+(?:\.\d+)?)\s*(hour|hours|hr|hrs)", text)
    if m:
        try:
            available_hours = float(m.group(1))
        except ValueError:
            pass

    # Workload heuristics
    assignments_pending = 1 if "assignment" in text or "homework" in text else 0
    if re.search(r"(\d+)\s+(assignment|assignments|hw|homework)", text):
        assignments_pending = int(re.search(r"(\d+)\s+(assignment|assignments|hw|homework)", text).group(1))

    labs_today = 1 if "lab" in text or "practical" in text else 0

    projects_active = any(k in text for k in ["project", "mini project", "major project"])

    upcoming_exam_in_days: Optional[int] = None
    exam_match = re.search(r"exam[^\d]*(in\s+)?(\d+)\s+(day|days)", text)
    if exam_match:
        upcoming_exam_in_days = int(exam_match.group(2))

    return plan_bca_day(
        location=location,
        available_hours=available_hours,
        assignments_pending=assignments_pending,
        labs_today=labs_today,
        projects_active=projects_active,
        upcoming_exam_in_days=upcoming_exam_in_days,
    )
