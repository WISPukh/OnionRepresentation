import sys

from onion_app.adapters.alembic.launcher import Runner
from onion_app.adapters.alembic.settings import Settings
from onion_app.adapters.database.settings import Settings as DBSettings
from onion_app.adapters.logging.alembic import get_logging_config

runner = Runner(
    settings=Settings,
    db_settings=DBSettings,
    logging_getter=get_logging_config
)
runner.run(*sys.argv[1:])
