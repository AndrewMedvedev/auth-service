from typing import TypeVar

from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.exc import DataError

from ..core.exeptions import AlreadyCreatedError, MismatchError
from ..core.schemas import UserResponse
from .base import Base
from .models import IdentityProviderModel, UserIdentityModel, UserModel
from .session import SQLSessionService

Model = TypeVar("Model", bound=Base)


class SQLRepository[Model: Base](SQLSessionService):
    model: type[Model]

    async def create(self, schema: BaseModel) -> UUID:
        try:
            async with self.session() as session:
                stmt = insert(self.model).values(**schema.model_dump()).returning(self.model.id)  # type: ignore  # noqa: PGH003
                result = await session.execute(stmt)
                await session.commit()
                return result.scalar_one()
        except DataError:
            await session.rollback()
            raise MismatchError from None
        except InterruptedError:
            await session.rollback()
            raise AlreadyCreatedError from None


class UserRepository(SQLRepository[UserModel]):
    model = UserModel

    async def get_by_email(self, email: str) -> UserResponse | None:
        async with self.session() as session:
            stmt = select(self.model.id, self.model.password).where(self.model.email == email)  # type: ignore  # noqa: PGH003
            result = await session.execute(stmt)
            model = result.mappings().first()
            return UserResponse.model_validate(model) if model else None


class UserIdentityRepository(SQLRepository[UserIdentityModel]):
    model = UserIdentityModel

    async def get_by_user_id(self, provider_user_id: str) -> UUID | None:
        async with self.session() as session:
            stmt = select(self.model.id).where(self.model.provider_user_id == provider_user_id)  # type: ignore  # noqa: PGH003
            result = await session.execute(stmt)
            return result.scalar_one_or_none()


class IdentityRepository(SQLRepository[IdentityProviderModel]):
    model = IdentityProviderModel

    async def get_by_name(self, name: str) -> UUID | None:
        async with self.session() as session:
            stmt = select(self.model.id).where(self.model.name == name)  # type: ignore  # noqa: PGH003
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
