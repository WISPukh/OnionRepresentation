from abc import ABC, abstractmethod
from typing import Type

from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from composites.postgres_db import Base


class DB(ABC):
    def __init__(self, session_db: AsyncSession, model: Type[Base]):
        self.session_db = session_db
        self.model = model

    @abstractmethod
    async def get(self): ...

    @abstractmethod
    async def save(self, instances, report): ...


class SourceApi(ABC):
    def __init__(self, base_url: str, aiohttp_session: ClientSession, page_size: int, auth_api: str):
        self.base_url = base_url
        self.aiohttp_session = aiohttp_session
        self.page_size = page_size
        self.auth_api = auth_api

    @abstractmethod
    def get(self): ...
