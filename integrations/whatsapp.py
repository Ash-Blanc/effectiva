"""WhatsApp-style integration tools for Effectiva.

These tools do *not* connect directly to WhatsApp yet.
Instead, they provide a thin abstraction for logging and
retrieving WhatsApp-like messages in Memori so that the
agent system can reason about conversations with key
contacts, crises, and commitments.

A future step can connect actual WhatsApp webhooks or
Twilio messaging to these helpers.
"""
from __future__ import annotations

from typing import Literal, Dict, Any

from memory.memory_manager import log_event


def log_whatsapp_message(
    contact: str,
    direction: Literal["inbound", "outbound"],
    content: str,
    context: str = "coordinator",
) -> str:
    """Log a WhatsApp-style message in Memori.

    Args:
        contact: Human-friendly name or identifier (e.g., "Mom", "CS Class Group").
        direction: "inbound" for messages from the contact, "outbound" for
            messages suggested or drafted by Effectiva.
        content: The message text.
        context: Memory context; defaults to "coordinator".
    """

    payload: Dict[str, Any] = {
        "contact": contact,
        "direction": direction,
        "content": content,
    }
    return log_event(context=context, event_type="whatsapp_message", payload=payload)
