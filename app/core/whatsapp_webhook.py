from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class InboundMessage:
    message_id: str
    phone: str
    text: str
    origin_type: str


def parse_inbound_messages(payload: dict[str, Any]) -> list[InboundMessage]:
    out: list[InboundMessage] = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            contacts = value.get("contacts", [{}])
            phone = contacts[0].get("wa_id", "") if contacts else ""
            for msg in value.get("messages", []):
                text = msg.get("text", {}).get("body", "")
                out.append(
                    InboundMessage(
                        message_id=msg.get("id", ""),
                        phone=phone,
                        text=text,
                        origin_type=msg.get("from", phone),
                    )
                )
    return out
