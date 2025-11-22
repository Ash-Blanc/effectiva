"""Toon-based domain models for Effectiva.

These helpers use the `python-toon` package to encode/decode
human-readable, LLM-friendly structures for tasks, schedules,
student profiles, and crisis episodes.

Note: We intentionally keep these models lightweight and
representation-focused; business logic lives in tools/ and
DSPy programs.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any

from toon import encode, decode  # type: ignore[import]


# -------------------------
# Core Toon data classes
# -------------------------


@dataclass
class Task:
    id: str
    title: str
    subject: Optional[str] = None
    kind: str = "general"  # e.g. assignment, lab, project, exam_prep, practice
    deadline: Optional[str] = None  # ISO date or datetime
    location: Optional[str] = None  # home, college, online, etc.
    duration_estimate_min: Optional[int] = None
    energy_level: Optional[str] = None  # low / medium / high
    dependencies: Optional[List[str]] = None
    status: str = "pending"  # pending / in_progress / completed


@dataclass
class ScheduleBlock:
    label: str
    tasks: List[Task]
    start_window: Optional[str] = None  # ISO datetime or human range, e.g. "evening"
    duration_min: Optional[int] = None
    location: Optional[str] = None  # home / college
    confidence: Optional[float] = None
    explanation: Optional[str] = None


@dataclass
class StudentProfile:
    persona: str = "bca_student"
    branch: str = "BCA"
    semester: Optional[int] = None
    typical_wake_time: Optional[str] = None
    typical_sleep_time: Optional[str] = None
    home_duty_pattern: Optional[str] = None  # short natural-language description
    study_preferences: Optional[Dict[str, Any]] = None


@dataclass
class CrisisEpisode:
    severity: str  # mild / moderate / severe
    days_missed: int
    labs_missed: int
    assignments_pending: int
    upcoming_exam_in_days: Optional[int] = None
    stress_level: Optional[str] = None  # low / medium / high / overwhelmed
    notes: Optional[str] = None


# -------------------------
# Toon helpers
# -------------------------


def _encode_dataclass(value: Any) -> str:
    """Encode any dataclass instance as a Toon string."""

    return encode(asdict(value))


def _decode_dataclass(toon_str: str) -> Any:
    """Decode a Toon string into a plain Python dict.

    Specific dataclass reconstruction is done by the caller.
    """

    return decode(toon_str)


def task_to_toon(task: Task) -> str:
    return _encode_dataclass(task)


def toon_to_task(toon_str: str) -> Task:
    data = _decode_dataclass(toon_str)
    return Task(**data)


def schedule_block_to_toon(block: ScheduleBlock) -> str:
    return _encode_dataclass(block)


def toon_to_schedule_block(toon_str: str) -> ScheduleBlock:
    data = _decode_dataclass(toon_str)
    # Reconstruct nested tasks explicitly
    tasks = [Task(**t) for t in data.get("tasks", [])]
    data["tasks"] = tasks
    return ScheduleBlock(**data)


def student_profile_to_toon(profile: StudentProfile) -> str:
    return _encode_dataclass(profile)


def toon_to_student_profile(toon_str: str) -> StudentProfile:
    data = _decode_dataclass(toon_str)
    return StudentProfile(**data)


def crisis_episode_to_toon(ep: CrisisEpisode) -> str:
    return _encode_dataclass(ep)


def toon_to_crisis_episode(toon_str: str) -> CrisisEpisode:
    data = _decode_dataclass(toon_str)
    return CrisisEpisode(**data)
