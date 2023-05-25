from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

PATH_BASE = Path(__file__).parent.parent.parent


class SourceApiSettings(BaseSettings):
    base_url: str
    is_jwt: bool = True
    email: str | None
    password: str | None

    class Config:
        env_file = f"{PATH_BASE.parent}/.env"


@lru_cache
def get_settings() -> SourceApiSettings:
    return SourceApiSettings()


settings = get_settings()
