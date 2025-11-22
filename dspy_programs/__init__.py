"""DSPy-based helper programs for Effectiva.

This package contains small, composable DSPy programs
(intent classification, task decomposition, schedule
planning, crisis assessment, etc.).

The initial implementation keeps DSPy optional: if no
LM is configured (e.g., no OPENAI_API_KEY), helpers
fall back to simple heuristic logic so the system
remains usable.
"""