from ..core.base import BaseOauth
from ..core.exeptions import BadRequestHTTPError
from ..core.schemas import Codes, YandexCallbackSchema, YandexRedirectSchema
from ..rest import YandexApi


class YandexControl(BaseOauth):
    name = "Yandex"

    def __init__(self) -> None:
        super().__init__(api=YandexApi())

    async def generate_url(self) -> str:
        codes = Codes.generate()
        await self.redis.add(codes.state, codes.code_verifier)
        return YandexRedirectSchema().to_url(
            state=codes.state, code_challenge=codes.code_challenge
        )

    async def authentication(self, schema: YandexCallbackSchema) -> dict:
        data = await self.callback(schema)
        user_data = await self.api.get_data(data.model_dump())
        user_id = await self.user_repository.get_by_user_id(user_data.provider_user_id)
        if user_id is not None:
            return await self.jwt.create_tokens(user_id=user_id)
        raise BadRequestHTTPError("User not found")
