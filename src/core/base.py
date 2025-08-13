from abc import ABC, abstractmethod
from logging import DEBUG, Formatter, Logger, StreamHandler, getLogger

from pydantic import BaseModel

from ..database.repository import IdentityRepository, UserIdentityRepository
from ..jwt import JWTCreate
from ..storage import RedisStorage
from .exeptions import NotFoundHTTPError
from .schemas import UserIdentitySchema


class LoggerMixin:
    logger: Logger = getLogger()

    @staticmethod
    def config_logging(logger: Logger) -> Logger:
        if not logger.handlers:
            handler = StreamHandler()
            formatter = Formatter(
                fmt="%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s",  # noqa: E501
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(DEBUG)
        return logger

    def __new__(cls, *_, **__):
        obj = super().__new__(cls)
        obj.logger = cls.logger.getChild(f"{cls.__name__}")
        cls.config_logging(obj.logger)
        return obj


class BaseOauthAPI(LoggerMixin, ABC):
    logger = getLogger("rest")

    @abstractmethod
    async def get_access_token(self, schema: dict) -> BaseModel: ...

    @abstractmethod
    async def get_data(self, schema: dict) -> UserIdentitySchema: ...


class BaseOauth(ABC):
    name: str

    def __init__(self, api: BaseOauthAPI) -> None:
        self.user_repository = UserIdentityRepository()
        self.identity_repository = IdentityRepository()
        self.redis = RedisStorage()
        self.api = api
        self.jwt = JWTCreate()

    @abstractmethod
    async def generate_url(self) -> str: ...

    async def callback(self, schema: BaseModel) -> BaseModel:
        code_verifier = await self.redis.get(schema.state)  # type: ignore  # noqa: PGH003
        return await self.api.get_access_token(schema.to_dict(code_verifier=code_verifier))  # type: ignore  # noqa: PGH003

    async def registration(self, schema: BaseModel) -> dict:
        data = await self.callback(schema)
        provider_id = await self.identity_repository.get_by_name(self.name)
        if provider_id is None:
            raise NotFoundHTTPError("Provider not found")
        user_data = await self.api.get_data(data.model_dump())
        user_data.provider_id = provider_id
        user_id = await self.user_repository.create(user_data)
        return await self.jwt.create_tokens(user_id=user_id)
