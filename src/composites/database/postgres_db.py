from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from adapters.db.settings import settings

Base = declarative_base()

engine = create_async_engine(settings.db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)  # noqa


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
