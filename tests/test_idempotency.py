from app.core.idempotency import is_duplicate_message


def test_idempotency(session) -> None:
    assert is_duplicate_message(session, "m1") is False
    assert is_duplicate_message(session, "m1") is True
