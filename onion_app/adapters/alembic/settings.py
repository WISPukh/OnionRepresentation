from pathlib import Path

from pydantic import BaseSettings

PATH_BASE = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    SA_LOGS: bool = True
    LOG_LEVEL: str = 'INFO'

    ALEMBIC_VERSION_LOCATION: str = 'onion_app.adapters.database:migrations'
    ALEMBIC_SCRIPT_LOCATION: str = 'onion_app.composites:alembic'
    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        '%%(year)d_%%(month).2d_'
        '%%(day).2d_%%(hour).2d_'
        '%%(minute).2d_%%(slug)s'
    )

    class Config:
        env_file_encoding = 'utf-8'
        env_file = f"{PATH_BASE.parent}/.env"
