"""Intent classification helper using DSPy where available.

This module exposes a single function, ``classify_intent``,
which returns a small dict with ``intent`` and ``confidence``
keys. It is designed to be wrapped as an Agno tool so that
agents (especially the Coordinator) can call it during
reasoning.

If DSPy or a configured LM is not available, we fall back
to simple keyword-based heuristics.
"""
from __future__ import annotations

from typing import Dict

from config.settings import OPENAI_API_KEY


_dspy_predictor = None


def _init_dspy_predictor() -> None:
    """Lazily configure DSPy predictor if possible.

    We only configure DSPy when an OpenAI API key is
    available. Otherwise, we leave ``_dspy_predictor``
    as ``None`` and rely on heuristics.
    """

    global _dspy_predictor
    if _dspy_predictor is not None:
        return

    if not OPENAI_API_KEY:
        return

    try:
        import dspy  # type: ignore[import]

        class IntentSignature(dspy.Signature):  # type: ignore[attr-defined]
            """Classify a student's request into a high-level intent.

            Allowed intents (must be one of these):
            - bca_crisis
            - bca_exam_prep
            - bca_assignment
            - bca_lab
            - generic_study
            - work
            - life
            - meta_productivity
            """

            message = dspy.InputField()  # type: ignore[attr-defined]
            intent = dspy.OutputField()  # type: ignore[attr-defined]
            confidence = dspy.OutputField()  # type: ignore[attr-defined]

        # Configure DSPy with a default OpenAI LM.
        dspy.configure(lm=dspy.OpenAI(api_key=GOOGLE_API_KEY))  # type: ignore[attr-defined]
        _dspy_predictor = dspy.Predict(IntentSignature)  # type: ignore[attr-defined]

    except Exception:
        # If anything goes wrong (missing dspy, misconfig),
        # we silently fall back to heuristics.
        _dspy_predictor = None


def _heuristic_intent(message: str) -> Dict[str, str]:
    """Very simple keyword-based intent classifier.

    This is intentionally conservative and BCA/student-centric.
    """

    text = message.lower()

    if any(k in text for k in ["panic", "stressed", "overwhelmed", "crisis", "behind"]):
        return {"intent": "bca_crisis", "confidence": "0.8"}

    if "exam" in text or "test" in text:
        return {"intent": "bca_exam_prep", "confidence": "0.75"}

    if any(k in text for k in ["assignment", "homework", "sheet", "submission"]):
        return {"intent": "bca_assignment", "confidence": "0.7"}

    if any(k in text for k in ["lab", "practical", "practicals"]):
        return {"intent": "bca_lab", "confidence": "0.7"}

    if any(k in text for k in ["project", "mini project", "major project"]):
        return {"intent": "generic_study", "confidence": "0.65"}

    if any(k in text for k in ["job", "shift", "office", "work shift"]):
        return {"intent": "work", "confidence": "0.6"}

    if any(k in text for k in ["family", "home chores", "chores", "cooking", "cleaning"]):
        return {"intent": "life", "confidence": "0.6"}

    if any(k in text for k in ["schedule", "plan my day", "productivity", "focus"]):
        return {"intent": "meta_productivity", "confidence": "0.6"}

    return {"intent": "generic_study", "confidence": "0.5"}


def classify_intent(message: str) -> Dict[str, str]:
    """Classify a free-form user message into a high-level intent.

    Returns a dict with ``intent`` and ``confidence`` (as a string).
    """

    _init_dspy_predictor()
    if _dspy_predictor is None:
        return _heuristic_intent(message)

    try:
        pred = _dspy_predictor(message=message)
        intent = getattr(pred, "intent", None) or "generic_study"
        confidence = getattr(pred, "confidence", None)
        if confidence is None:
            confidence_str = "0.7"
        else:
            confidence_str = str(confidence)
        return {"intent": str(intent), "confidence": confidence_str}
    except Exception:
        # Fall back gracefully on any runtime errors.
        return _heuristic_intent(message)
