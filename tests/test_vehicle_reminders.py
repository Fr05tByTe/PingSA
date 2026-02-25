from datetime import date, timedelta

from app.core.models import User
from app.modules.vehicle.service import add_vehicle, reminders_due


def test_vehicle_reminder_due(session) -> None:
    user = User(phone="27820000001")
    session.add(user)
    session.commit()
    add_vehicle(session, user, "CA12345", date.today() + timedelta(days=30), [30, 7])
    due = reminders_due(session, date.today())
    assert len(due) == 1
    assert due[0][2] == 30
