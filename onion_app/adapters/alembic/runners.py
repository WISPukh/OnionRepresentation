from sqlalchemy import create_engine, pool


def run_migrations_offline(config, context, target_metadata):
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        include_schemas=True,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online(config, context, target_metadata):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            compare_type=True,
            version_table_schema=target_metadata.schema,
        )

        with context.begin_transaction():
            connection.execute(
                f"if schema_id('{target_metadata.schema}') is null "
                f"execute('create schema {target_metadata.schema}')"
            )
            context.run_migrations()
