from typing import Optional, Any
from functools import lru_cache

from pydantic import BaseSettings, validator, PostgresDsn
from pathlib import Path


PATH_BASE = Path(__file__).parent.parent.parent


class DBSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    DATABASE_NAME: str = ''
    db_url: str | None

    class Config:
        env_file = f"{PATH_BASE.parent}/.env"

    @validator('db_url', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> str:  # noqa
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            port=values.get('POSTGRES_PORT'),
            path=f"/{values.get('DATABASE_NAME')}",
        )


@lru_cache
def get_settings() -> DBSettings:
    return DBSettings()


settings = get_settings()
