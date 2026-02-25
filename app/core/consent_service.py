from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.core.models import User


def set_consent(db: Session, user: User, version: str) -> None:
    user.consent_version = version
    user.consent_timestamp = datetime.utcnow()
    db.commit()
