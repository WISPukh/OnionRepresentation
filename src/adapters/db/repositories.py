import logging
from typing import Type, Any, Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, delete

from application.ETL.dto import BookDTO
from application.interfaces import BookRepository as BaseDB
from composites.database.postgres_db import Base


class BookRepository(BaseDB):
    def __init__(self, session_db: AsyncSession, model: Type[Base]):
        self.session_db = session_db
        self.model = model

    async def get_all(self) -> Sequence[Any]:
        return (await self.session_db.execute(select(self.model))).scalars().all()

    def _dto_to_model(self, instances: list) -> list[BookDTO]:
        models = []
        for instance in instances:
            try:
                models.append(self.model(**instance.dict_repr()))
            except TypeError as exc:
                logging.error(exc)
        return models

    async def save(self, instances: list) -> bool:
        instances = self._dto_to_model(instances)
        await self.session_db.execute(delete(self.model))
        self.session_db.add_all(instances)
        try:
            await self.session_db.commit()
        except SQLAlchemyError as exc:
            logging.error(exc)
            return False

        return True
