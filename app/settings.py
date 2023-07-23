import secrets
from functools import lru_cache

from pydantic_settings import BaseSettings

from app.schemas.settings import Environment


class Settings(BaseSettings):
    access_token_expire_minutes: int = 10
    api_debug: bool = True
    api_disable_docs: bool = False
    environment: Environment = "development"
    refresh_token_expire_minutes: int = 30
    sql_alchemy_database_url: str = "sqlite:///././sql_database.db"
    token_generator_secret_key: str = secrets.token_hex(64)

    class ConfigDict:
        env_file = ".env"
        env_file_encoding = "utf-8"
        use_enum_values = True


@lru_cache()
def get_settings():
    return Settings()
