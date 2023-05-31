from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, PositiveInt

PATH_BASE = Path(__file__).parent.parent.parent


class CronSettings(BaseSettings):
    CRON_SECOND: PositiveInt

    class Config:
        env_file = f"{PATH_BASE.parent}/.env"


@lru_cache
def get_settings() -> CronSettings:
    return CronSettings()


settings = get_settings()
