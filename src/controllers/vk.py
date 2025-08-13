from ..core.base import BaseOauth
from ..core.exeptions import BadRequestHTTPError
from ..core.schemas import Codes, VKCallbackSchema, VKRedirectSchema
from ..rest import VKApi


class VKControl(BaseOauth):
    name = "VK"

    def __init__(self) -> None:
        super().__init__(api=VKApi())

    async def generate_url(self) -> str:
        codes = Codes.generate()
        await self.redis.add(codes.state, codes.code_verifier)
        return VKRedirectSchema().to_url(state=codes.state, code_challenge=codes.code_challenge)

    async def authentication(self, schema: VKCallbackSchema) -> dict:
        data = await self.callback(schema)
        user_id = await self.user_repository.get_by_user_id(data.user_id)  # type: ignore  # noqa: PGH003
        if user_id is not None:
            return await self.jwt.create_tokens(user_id=user_id)
        raise BadRequestHTTPError("User not found")
