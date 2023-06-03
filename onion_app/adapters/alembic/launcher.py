import logging.config
import os
from typing import Callable

from alembic.config import CommandLine, Config


class Runner:

    def __init__(
        self,
        settings: Callable,
        db_settings: Callable,
        logging_getter: Callable,
    ):
        self._settings = settings
        self._db_settings = db_settings
        self._logging_getter = logging_getter

    def run(self, *args):
        dev_config = os.getenv('DEV_CONFIG')

        if dev_config:
            settings = self._settings(_env_file=dev_config)
            db_settings = self._db_settings(_env_file=dev_config)
        else:
            settings = self._settings()
            db_settings = self._db_settings()

        logging_config = self._get_logging_config(settings)
        logging.config.dictConfig(logging_config)

        cli = CommandLine()
        cli.run_cmd(
            self._make_config(db_settings, settings),
            cli.parser.parse_args(args),
        )

    def _get_logging_config(self, settings):
        return self._logging_getter(
            log_level=settings.LOG_LEVEL,
            sa_logs=settings.SA_LOGS,
        )

    @staticmethod
    def _make_config(db_settings, settings):
        config = Config()
        config.set_main_option('timezone', 'UTC')
        config.set_main_option(
            'sqlalchemy.url',
            db_settings.db_url,
        )
        config.set_main_option(
            'script_location',
            settings.ALEMBIC_SCRIPT_LOCATION,
        )
        config.set_main_option(
            'version_locations',
            settings.ALEMBIC_VERSION_LOCATION,
        )
        config.set_main_option(
            'file_template',
            settings.ALEMBIC_MIGRATION_FILENAME_TEMPLATE,
        )

        return config
