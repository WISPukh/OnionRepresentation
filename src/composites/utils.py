import asyncio
import logging

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.dashboard import api
from adapters.db.models import Book
from adapters.db.repositories import BookRepository
from adapters.source_api.repositories import SourceApi
from adapters.source_api.settings import settings
from application.ETL.services import ETL
from composites.database.postgres_db import get_session


async def get_repo(session: AsyncSession) -> BookRepository:
    return BookRepository(session_db=session, model=Book)


async def get_source_api(page_size: int = 100, is_jwt: bool = True) -> SourceApi:
    return SourceApi(page_size, is_jwt)


async def get_etl(repository: BookRepository, source_api: SourceApi):
    return ETL(repository, source_api)


async def get_connection(func):
    return await anext(func)


async def main() -> FastAPI:
    postgres_session = await get_connection(get_session())  # noqa
    repository = await get_repo(postgres_session)
    source_api = await get_source_api(is_jwt=settings.is_jwt)
    etl = await get_etl(repository, source_api)
    return api.get_app(etl=etl)


async def root():
    return {"message": "Server is running!"}


logging.basicConfig(
    format='%(pathname)s\n%(asctime)s LINE NUMBER - %(lineno)d: FUNCTION - %(funcName)s \n %(message)s\n',
    datefmt='(%I:%M:%S %p)',
    filename='errors.log',
    encoding='utf-8',
    level=logging.ERROR
)
logger = logging.Logger('main_logger')

if __name__ == '__main__':
    app = asyncio.run(main())
    app.add_api_route('/', endpoint=root)  # noqa
    uvicorn.run(app)
