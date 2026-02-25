from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

TZ_JHB = ZoneInfo("Africa/Johannesburg")


def now_jhb() -> datetime:
    return datetime.now(tz=TZ_JHB)
