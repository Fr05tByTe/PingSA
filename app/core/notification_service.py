from __future__ import annotations

from app.core.whatsapp_payloads import build_text


def friendly_cooldown(phone: str) -> dict[str, object]:
    return build_text(phone, "You're sending messages quickly. Please wait a moment and try again.")
