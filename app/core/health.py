from __future__ import annotations

from redis import Redis
from sqlalchemy import text
from sqlalchemy.orm import Session


def live() -> dict[str, str]:
    return {"status": "ok"}


def ready(db: Session, redis_client: Redis) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    redis_client.ping()
    return {"status": "ready"}
