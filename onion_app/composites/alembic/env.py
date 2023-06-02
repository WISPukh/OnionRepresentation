from alembic import context

from onion_app.adapters.alembic.runners import (
    run_migrations_offline,
    run_migrations_online,
)
from onion_app.adapters.database.models import Base
from onion_app.adapters.database.models import Book # noqa

config = context.config

if context.is_offline_mode():
    run_migrations_offline(
        config=config,
        context=context,
        target_metadata=Base.metadata,
    )
else:
    run_migrations_online(
        config=config,
        context=context,
        target_metadata=Base.metadata,
    )
