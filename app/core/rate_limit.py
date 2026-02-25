from __future__ import annotations

from redis import Redis


def check_rate_limit(redis_client: Redis, key: str, limit_per_minute: int) -> bool:
    redis_key = f"ratelimit:{key}"
    pipe = redis_client.pipeline()
    pipe.incr(redis_key)
    pipe.expire(redis_key, 60)
    count, _ = pipe.execute()
    return int(count) <= limit_per_minute
