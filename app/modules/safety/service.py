from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import SafetyContact, SafetyEvent, SafetySession


def start_timer(db: Session, user_id: object, mode: str, minutes: int) -> SafetySession:
    now = datetime.utcnow()
    session = SafetySession(user_id=user_id, mode=mode, duration_minutes=minutes, started_at=now, ends_at=now + timedelta(minutes=minutes), status="active")
    db.add(session)
    db.flush()
    db.add(SafetyEvent(safety_session_id=session.id, event_type="start", payload_json={"mode": mode}))
    db.commit()
    db.refresh(session)
    return session


def checkin(db: Session, session: SafetySession) -> None:
    session.last_checkin_at = datetime.utcnow()
    db.add(SafetyEvent(safety_session_id=session.id, event_type="checkin", payload_json={}))
    db.commit()


def tick_expired(db: Session, now: datetime) -> list[SafetySession]:
    sessions = db.scalars(select(SafetySession).where(SafetySession.status == "active", SafetySession.ends_at <= now)).all()
    for sess in sessions:
        sess.status = "escalated"
        db.add(SafetyEvent(safety_session_id=sess.id, event_type="escalate", payload_json={}))
    db.commit()
    return sessions


def active_contacts(db: Session, user_id: object) -> list[SafetyContact]:
    return db.scalars(select(SafetyContact).where(SafetyContact.user_id == user_id, SafetyContact.active.is_(True))).all()
