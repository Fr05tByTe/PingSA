from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import User


def get_or_create_user(db: Session, phone: str) -> User:
    user = db.scalar(select(User).where(User.phone == phone))
    if user:
        return user
    user = User(phone=phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_last_inbound(db: Session, user: User) -> None:
    user.last_inbound_at = datetime.utcnow()
    db.commit()
