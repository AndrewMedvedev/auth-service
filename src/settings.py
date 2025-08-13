from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)


class SqlSettings(BaseSettings):
    postgres_host: str = ""
    postgres_port: int = 5432
    postgres_password: str = ""
    postgres_user: str = ""
    postgres_db: str = ""

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


class RedisSettings(BaseSettings):
    redis_host: str = ""
    redis_port: int = 6379


class VKSettings(BaseSettings):
    vk_app_id: str = ""
    vk_app_secret: str = ""
    vk_client_secret: str = ""
    vk_redirect_uri: str = ""
    vk_auth_url: str = ""
    vk_token_url: str = ""
    vk_api_url: str = ""


class YandexSettings(BaseSettings):
    yandex_app_id: str = ""
    yandex_app_secret: str = ""
    yandex_auth_url: str = ""
    yandex_token_url: str = ""
    yandex_api_url: str = ""


class SecretSettings(BaseSettings):
    secret_key: str = ""
    secret_key_hash: str = ""


class Settings(BaseSettings):
    sql_settings: SqlSettings = SqlSettings()
    redis_settings: RedisSettings = RedisSettings()
    vk_settings: VKSettings = VKSettings()
    yandex_settings: YandexSettings = YandexSettings()
    secret_settings: SecretSettings = SecretSettings()


settings = Settings()
