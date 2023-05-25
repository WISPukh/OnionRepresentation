from aiohttp import ClientSession
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.db.models import Book
from adapters.db.repositories import BookRepository
from adapters.source_api.repositories import SourceApi
from adapters.source_api.settings import settings
from application.ETL.services import ETL
from composites import aiohttp_session
from composites.database import postgres_db


async def get_db(session: AsyncSession = Depends(postgres_db.get_session)) -> BookRepository:
    return BookRepository(session_db=session, model=Book)


async def get_source_api(
        session: ClientSession = Depends(aiohttp_session.get_session),
        page_size: int = 100
) -> SourceApi:
    return SourceApi(session, page_size, settings.is_jwt)


async def get_etl(db: BookRepository = Depends(get_db), source_api: SourceApi = Depends(get_source_api)):
    return ETL(db, source_api)
