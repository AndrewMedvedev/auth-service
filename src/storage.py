from redis.asyncio import Redis

from .settings import settings


class RedisStorage:
    session = Redis(
        host=settings.redis_settings.redis_host,
        port=settings.redis_settings.redis_port,
        decode_responses=True,
    )

    async def add(self, state: str, code_verifier: str) -> None:
        await self.session.setex(name=state, value=code_verifier, time=400)

    async def get(self, key: str) -> str:
        result = await self.session.get(key)
        await self.session.delete(key)
        return result
