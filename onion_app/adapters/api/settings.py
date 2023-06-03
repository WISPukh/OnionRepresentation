from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

PATH_BASE = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    SERVER_PORT: int
    SERVER_HOST: str
    DEBUG: bool
    RELOAD_DIRS: str

    class Config:
        env_file = f"{PATH_BASE.parent}/.env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

