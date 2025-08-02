from ..database import SQLRegistration
from ..exeptions import BadRequestHTTPError
from ..jwt import JWTCreate
from ..schemas import UserSchema
from ..utils import Hash


class AuthControl:
    def __init__(self) -> None:
        self.sql = SQLRegistration()
        self.jwt = JWTCreate()
        self.hash = Hash()

    async def registration(self, schema: UserSchema) -> dict:
        user_id = await self.sql.create_user(schema.to_model)
        return await self.jwt.create_tokens(user_id=user_id)

    async def login_email(self, schema: UserSchema) -> dict:
        stmt = await self.sql.get_user_email(schema.email)
        if self.hash.verify_password(schema.password, stmt.password):
            return await self.jwt.create_tokens(stmt.id)
        raise BadRequestHTTPError(message="wrong password")
