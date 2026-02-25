from datetime import datetime, timedelta

from app.core.models import User
from app.modules.safety.service import start_timer, tick_expired


def test_safety_escalation_once(session) -> None:
    user = User(phone="27820000003")
    session.add(user)
    session.commit()
    sess = start_timer(session, user.id, "jogging", 1)
    sess.ends_at = datetime.utcnow() - timedelta(minutes=1)
    session.commit()
    expired = tick_expired(session, datetime.utcnow())
    assert len(expired) == 1
    expired2 = tick_expired(session, datetime.utcnow())
    assert len(expired2) == 0
