from __future__ import annotations

from app.core.models import SafetyContact, SafetySession


def escalation_messages(session: SafetySession, contacts: list[SafetyContact], user_phone: str) -> list[str]:
    _ = session
    return [f"PingSA Safety Alert: No check-in from {user_phone} after safety timer. Please contact them." for _ in sorted(contacts, key=lambda c: c.priority)]
