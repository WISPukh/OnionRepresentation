import logging.config

import uvicorn
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.background import BackgroundTask

from onion_app.adapters.api.controllers import configure_app
from onion_app.adapters.api.settings import settings as api_settings
from onion_app.adapters.api.exception_handlers import handle_exceptions
from onion_app.adapters.database.models import Book
from onion_app.adapters.database.repositories import BookRepository
from onion_app.adapters.database.settings import settings as db_settings
from onion_app.adapters.scheduler.runner import Scheduler
from onion_app.adapters.scheduler.settings import settings as scheduler_settings
from onion_app.adapters.source_api.repositories import SourceApi
from onion_app.adapters.source_api.settings import settings as source_api_settings
from onion_app.adapters.logging.configs import LOGGING_CONFIG
from onion_app.application.exceptions import BaseError
from onion_app.application.ETL.services import ETL

logging.config.dictConfig(LOGGING_CONFIG)
info_logger = logging.getLogger('info_logger')


class DB:
    engine = create_async_engine(db_settings.db_url, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_book_repo(session: AsyncSession) -> BookRepository:
    return BookRepository(session_db=session, model=Book)


async def get_source_api(page_size: int = 100, is_jwt: bool = True) -> SourceApi:
    return SourceApi(
        page_size=page_size,
        base_url=source_api_settings.base_url,
        email=source_api_settings.email,
        password=source_api_settings.password,
        is_jwt=is_jwt
    )


async def get_etl(repository: BookRepository, source_api: SourceApi) -> ETL:
    return ETL(repository, source_api)


@repeat_every(seconds=scheduler_settings.CRON_SECOND, logger=logging.getLogger())
async def call_process():
    scheduler = Scheduler.get_instance()
    info_logger.info(f"Task {scheduler.task.__qualname__} started!")
    await scheduler.execute()


app = FastAPI()
if not api_settings.DEBUG:
    app.add_exception_handler(BaseError, handle_exceptions)


@app.on_event('startup')
async def setup():
    async with DB.SessionLocal() as session:
        book_repo = await get_book_repo(session)
        source_api = await get_source_api(is_jwt=source_api_settings.is_jwt)
        etl = await get_etl(book_repo, source_api)

        configure_app(app=app, book_repo=book_repo)
        Scheduler.get_instance(task=etl.process)
        task = BackgroundTask(call_process)

        await task()


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        reload_dirs=api_settings.RELOAD_DIRS,
        reload=True,
        port=api_settings.SERVER_PORT,
        host=api_settings.SERVER_HOST
    )
