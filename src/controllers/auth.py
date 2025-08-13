from ..core.exeptions import BadRequestHTTPError
from ..core.schemas import UserSchema
from ..core.utils import Hash
from ..database.repository import UserRepository
from ..jwt import JWTCreate


class AuthControl:
    def __init__(self) -> None:
        self.repository = UserRepository()
        self.jwt = JWTCreate()
        self.hash = Hash()

    async def registration(self, schema: UserSchema) -> dict:
        user_id = await self.repository.create(schema)
        return await self.jwt.create_tokens(user_id=user_id)

    async def authentication(self, schema: UserSchema) -> dict:
        stmt = await self.repository.get_by_email(schema.email)
        if stmt is None:
            raise BadRequestHTTPError(message="wrong email")
        if self.hash.verify_password(schema.password.get_secret_value(), stmt.password):
            return await self.jwt.create_tokens(stmt.id)
        raise BadRequestHTTPError(message="wrong password")
