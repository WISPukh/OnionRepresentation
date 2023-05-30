from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, root_validator

from exceptions import InternalServerError

PATH_BASE = Path(__file__).parent.parent.parent


class CronSettings(BaseSettings):
    CRON_SECOND: None | int = None

    @root_validator
    def check_only_one(cls, values: dict):
        if values['CRON_SECOND'] <= 0:
            raise InternalServerError("Ошибка сборки, неверно задан параметр CRON_SECOND")
        return values

    class Config:
        env_file = f"{PATH_BASE.parent}/.env"


@lru_cache
def get_settings() -> CronSettings:
    return CronSettings()


settings = get_settings()
