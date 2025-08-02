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
    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


class SecretSettings(BaseSettings):
    secret_key: str = ""
    secret_key_hash: str = ""


class Settings(BaseSettings):
    sql_settings: SqlSettings = SqlSettings()
    secret_settings: SecretSettings = SecretSettings()


settings = Settings()
