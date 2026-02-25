from __future__ import annotations

from app.core.constants import CONSENT_TEXT, WELCOME_BODY, WELCOME_HEADER
from app.core.whatsapp_payloads import build_buttons, build_list, build_text


def main_menu_payload(phone: str) -> dict[str, object]:
    return build_list(
        to=phone,
        header=WELCOME_HEADER,
        body=WELCOME_BODY,
        footer="Reply MENU anytime",
        sections=[
            {
                "title": "Main",
                "rows": [
                    {"id": "fines_setup", "title": "Traffic Fines (Auto-check)", "description": "Get notified when fines change"},
                    {"id": "vehicle_setup", "title": "Vehicle License Alerts", "description": "Expiry reminders before it’s due"},
                    {"id": "property_menu", "title": "Property Search", "description": "Find homes + contact agents"},
                    {"id": "safety_menu", "title": "Safety Timer (Jog/Walk)", "description": "Auto-alert contacts if no check-in"},
                    {"id": "help", "title": "Help", "description": "How PingSA works"},
                ],
            }
        ],
    )


def route_text(phone: str, text: str) -> list[dict[str, object]]:
    command = text.strip().upper()
    if text.strip().lower() == "hi" or command == "MENU":
        return [main_menu_payload(phone)]
    if command == "HELP":
        return [build_text(phone, "Use MENU to get started. Global commands: PAUSE, RESUME, CHECK, SAFE, EXTEND, SOS.")]
    if command == "PAUSE":
        return [build_text(phone, "All proactive alerts paused. Reply RESUME to restart.")]
    if command == "RESUME":
        return [build_text(phone, "Alerts resumed ✅")]
    if command in {"STOP FINES", "STOP"}:
        return [build_text(phone, "Fine monitoring disabled.")]
    if command == "DELETE DATA":
        return [build_buttons(phone, "Are you sure you want to delete your data?", [{"id": "delete_confirm_1", "title": "Yes"}, {"id": "delete_cancel", "title": "No"}])]
    if command == "CONSENT":
        return [build_buttons(phone, CONSENT_TEXT, [{"id": "consent_yes", "title": "I Agree"}, {"id": "consent_no", "title": "Not Now"}])]
    return [build_text(phone, "Got it. Reply MENU to continue.")]
