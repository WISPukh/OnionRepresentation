import json
import logging

from pydantic.error_wrappers import ValidationError

from application.ETL.dto import BookDTO
from application.interfaces import BookRepository, SourceApi


class ETL:
    def __init__(self, repository: BookRepository, source_api: SourceApi):
        self.repository = repository
        self.source_api = source_api

    @staticmethod
    def _transform(data: str) -> list[BookDTO]:
        json_data = json.loads(data)
        res = json_data['result']
        dto_instances: list = []
        for item in res:
            try:
                dto_instances.append(BookDTO(**item))  # noqa
            except ValidationError as exc:
                logging.error(exc)
        return dto_instances

    async def process(self):
        json_datas = await self.source_api.get()
        model_instances = self._transform(json_datas)
        return await self.repository.save(model_instances)
