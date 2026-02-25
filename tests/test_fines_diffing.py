from datetime import datetime, timedelta

from app.core.models import Fine, User
from app.modules.fines.service import upsert_and_diff_fines


def test_fine_diff_new_and_cooldown(session) -> None:
    user = User(phone="27820000002")
    session.add(user)
    session.commit()
    incoming = [{"plate": "CA1", "provider_reference": "X1", "offence_summary": "Speed", "amount": 100.0, "offence_date": None, "due_date": None, "status": "new"}]
    changed = upsert_and_diff_fines(session, user.id, incoming)
    assert len(changed) == 1
    fine = session.query(Fine).first()
    assert fine is not None
    fine.last_notified_at = datetime.utcnow()
    session.commit()
    changed2 = upsert_and_diff_fines(session, user.id, incoming)
    assert len(changed2) == 0
