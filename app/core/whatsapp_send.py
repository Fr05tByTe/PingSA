from __future__ import annotations

from datetime import timedelta
from typing import Any

import httpx

from app.core.time_utils import now_jhb


class WhatsAppSender:
    def __init__(self, token: str, phone_number_id: str) -> None:
        self.token = token
        self.phone_number_id = phone_number_id

    async def send(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"https://graph.facebook.com/v20.0/{self.phone_number_id}/messages"
        headers = {"Authorization": f"Bearer {self.token}"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            return resp.json()

    async def template_send(self, to: str, template_name: str) -> None:
        _ = (to, template_name, now_jhb() + timedelta(hours=24))
        # TODO: implement approved template sending flow.
