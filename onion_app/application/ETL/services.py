import json
import logging

from pydantic.error_wrappers import ValidationError

from onion_app.application.dto import BookDTO
from onion_app.application.exceptions import InternalServerError
from . import interfaces


class ETL:
    def __init__(
        self,
        repository: interfaces.BookRepository,
        source_api: interfaces.SourceApi,
    ):
        self._repository = repository
        self._source_api = source_api

    @staticmethod
    def _transform(data: str) -> list[BookDTO]:
        json_data = json.loads(data)
        res = json_data['result']
        dto_instances: list = []
        for item in res:
            try:
                dto_instances.append(BookDTO(**item))  # noqa
            except (TypeError, ValidationError) as exc:
                logging.error(exc)
                raise InternalServerError('Ошибка преобразования в DTO')
        return dto_instances

    async def process(self):
        json_datas = await self._source_api.get()
        dto_instances = self._transform(json_datas)
        return await self._repository.save(dto_instances)
