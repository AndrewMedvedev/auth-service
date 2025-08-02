from sqlalchemy import select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import DataError, IntegrityError

from ..exeptions import BadRequestHTTPError, ExistsHTTPError
from ..schemas import GetUserResponse
from .models import UserModel
from .session import SQLSessionService


class SQLRegistration(SQLSessionService):
    async def create_user(self, model: UserModel) -> UUID:
        try:
            async with self.session() as session:
                session.add(model)
                await session.commit()
                await session.refresh(model)
                return model.id
        except DataError:
            raise BadRequestHTTPError from None
        except IntegrityError:
            raise ExistsHTTPError from None

    async def get_user_email(self, email: str) -> GetUserResponse:
        try:
            async with self.session() as session:
                data = await session.execute(
                    select(UserModel.password, UserModel.id).where(UserModel.email == email)
                )
                result = data.mappings().first()
                if result is None:
                    raise BadRequestHTTPError("wrong email")
                return GetUserResponse(**result)
        except DataError:
            raise BadRequestHTTPError from None
