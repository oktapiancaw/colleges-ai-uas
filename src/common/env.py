from typing import Optional, Union

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore", env_prefix=""
    )

    RAPIDAPI_KEY: str
    RAPIDAPI_HOST: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE: int


def env_settings(other_env: str = None) -> Settings:
    if other_env:
        return Settings(_env_file=other_env)
    return Settings()


envs = env_settings()
