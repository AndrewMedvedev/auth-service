from datetime import UTC, datetime, timedelta
from uuid import uuid4

from jose import jwt
from sqlalchemy.dialects.postgresql import UUID

from .settings import settings


class JWTCreate:
    @staticmethod
    async def create_access(data: dict) -> str:
        data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid4())}
        data["exp"] = timedelta(hours=2) + datetime.now(tz=UTC)
        data["mode"] = "access_token"
        return jwt.encode(data, settings.secret_settings.secret_key, "HS256")

    @staticmethod
    async def create_refresh(data: dict) -> str:
        data["header"] = {"alg": "HS256", "typ": "JWT", "uuid": str(uuid4())}
        data["exp"] = timedelta(hours=5) + datetime.now(tz=UTC)
        data["mode"] = "refresh_token"
        return jwt.encode(data, settings.secret_settings.secret_key, "HS256")

    async def create_tokens(self, user_id: UUID) -> dict[str, str]:
        data = {"user_id": str(user_id)}
        access = await self.create_access(data)
        refresh = await self.create_refresh(data)
        return {
            "access": access,
            "refresh": refresh,
        }
