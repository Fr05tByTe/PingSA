from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.models import Reminder, User, Vehicle


def add_vehicle(db: Session, user: User, plate: str, expiry: date, schedule: list[int]) -> Vehicle:
    vehicle = Vehicle(user_id=user.id, plate=plate.upper(), license_expiry_date=expiry)
    db.add(vehicle)
    db.flush()
    db.add(Reminder(user_id=user.id, target_id=vehicle.id, rule_json=schedule, last_sent_at_json={}))
    db.commit()
    db.refresh(vehicle)
    return vehicle


def due_windows(expiry: date, today: date, windows: list[int]) -> list[int]:
    delta = (expiry - today).days
    return [w for w in windows if delta == w]


def reminders_due(db: Session, today: date) -> list[tuple[User, Vehicle, int, Reminder]]:
    items: list[tuple[User, Vehicle, int, Reminder]] = []
    reminders = db.scalars(select(Reminder).where(Reminder.enabled.is_(True))).all()
    for reminder in reminders:
        user = db.get(User, reminder.user_id)
        vehicle = db.get(Vehicle, reminder.target_id)
        if not user or not vehicle or user.notifications_paused:
            continue
        for window in due_windows(vehicle.license_expiry_date, today, reminder.rule_json):
            if str(window) not in reminder.last_sent_at_json:
                items.append((user, vehicle, window, reminder))
    return items
