import fakeredis

from app.core.rate_limit import check_rate_limit


def test_rate_limit() -> None:
    redis_client = fakeredis.FakeRedis(decode_responses=True)
    assert check_rate_limit(redis_client, "u1", 2)
    assert check_rate_limit(redis_client, "u1", 2)
    assert not check_rate_limit(redis_client, "u1", 2)
