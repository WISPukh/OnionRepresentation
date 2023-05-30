import logging.config

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.dashboard import api
from adapters.db.models import Book
from adapters.db.repositories import BookRepository
from adapters.source_api.repositories import SourceApi
from adapters.source_api.settings import settings as api_settings
from application.ETL.services import ETL
from composites.database.postgres_db import SessionLocal
from composites.settings_app import settings as app_settings, LOGGING_CONFIG
from exception_handlers import handle_exceptions
from exceptions import BaseError


async def get_repo(session: AsyncSession) -> BookRepository:
    return BookRepository(session_db=session, model=Book)


async def get_source_api(page_size: int = 100, is_jwt: bool = True) -> SourceApi:
    return SourceApi(page_size, is_jwt)


async def get_etl(repository: BookRepository, source_api: SourceApi) -> ETL:
    return ETL(repository, source_api)


logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI()

if not app_settings.DEBUG:
    app.add_exception_handler(BaseError, handle_exceptions)


@app.on_event('startup')
async def setup():
    async with SessionLocal() as session:
        repository = await get_repo(session)
        source_api = await get_source_api(is_jwt=api_settings.is_jwt)
        etl = await get_etl(repository, source_api)
        api.configure_app(app, etl=etl)


@app.get('/')
async def root():
    return {"message": "Server is running!"}


if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        reload_dirs='..',
        reload=True,
        port=app_settings.SERVER_PORT,
        host=app_settings.SERVER_HOST
    )
