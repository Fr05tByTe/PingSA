from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import Fine


def upsert_and_diff_fines(db: Session, user_id: object, incoming: list[dict[str, object]]) -> list[Fine]:
    changed: list[Fine] = []
    for item in incoming:
        ref = str(item.get("provider_reference") or "")
        existing = db.scalar(select(Fine).where(Fine.user_id == user_id, Fine.provider_reference == ref))
        if not existing:
            fine = Fine(user_id=user_id, **item)
            db.add(fine)
            changed.append(fine)
            continue
        meaningful = (float(existing.amount) != float(item["amount"])) or (existing.status != item["status"]) or (existing.due_date != item["due_date"])
        existing.last_seen_at = datetime.utcnow()
        if meaningful:
            existing.amount = item["amount"]
            existing.status = item["status"]
            existing.due_date = item["due_date"]
            changed.append(existing)
    db.commit()
    return [f for f in changed if not f.last_notified_at or f.last_notified_at < datetime.utcnow() - timedelta(hours=24)]
