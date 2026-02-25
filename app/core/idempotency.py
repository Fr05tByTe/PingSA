from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import InboundDedup


def is_duplicate_message(db: Session, message_id: str) -> bool:
    existing = db.scalar(select(InboundDedup).where(InboundDedup.message_id == message_id))
    if existing:
        return True
    db.add(InboundDedup(message_id=message_id))
    db.commit()
    return False
