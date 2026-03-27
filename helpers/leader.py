import asyncio
import aioredis
import time

LOCK_KEY = "bot_leader"
LOCK_TTL = 10  # seconds

async def try_acquire_lock(redis_url: str, instance_id: str):
    redis = await aioredis.from_url(redis_url)

    acquired = await redis.set(LOCK_KEY, instance_id, ex=LOCK_TTL, nx=True)

    return acquired is not None

async def refresh_lock(redis_url: str, instance_id: str):
    redis = await aioredis.from_url(redis_url)

    cur=redis.get(LOCK_KEY)
    if cur and cur.decode() == instance_id:
        await redis.expire(LOCK_KEY, LOCK_TTL)
        return True
    return False   

