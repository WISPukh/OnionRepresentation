import json
from typing import Optional

import aiohttp
from pydantic import dataclasses
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import session


class ETL:
    def __init__(
            self, session_db: session, source_api, auth_api: str, dto: dataclasses.dataclass, model, page_size: int
    ):
        self.session_db = session_db
        self.source_api = source_api
        self.auth_api = auth_api
        self.dto = dto
        self.report: str = ""
        self.model = model
        self.page_size = page_size

    async def extract(self):
        headers = {'Authorization': f'Bearer {self.auth_api}'}
        url = self.source_api + f"?page_size={self.page_size}"

        async with aiohttp.ClientSession() as session:
            response = await session.get(url=url, headers=headers)
            return await response.text()

    async def transform(self, data: str) -> list[dataclasses.dataclass]:
        json_data = json.loads(data)
        res = json_data['results']
        model_instances: list = []
        for item in res:
            dto_instance: Optional[dataclasses.dataclass] = None
            try:
                dto_instance = self.dto(
                    id=item['id'],
                    in_stock=item['in_stock'],
                    title=item['title'],
                    description=item['description'],
                    price=item['price'],
                    genres=item['genres'],
                    author=item['author'],
                    release_date=item['release_date'],
                    writing_date=item['writing_date']
                )
            except ValidationError as e:
                self.report += f"{e} \n"
            try:
                model_instances.append(self.model(**dto_instance.dict_repr()))
            # TODO: change exceptions
            except Exception as e:
                self.report += f"{e} \n"

        return model_instances

    async def load(self, instances: list):
        # is_success = True
        try:
            self.session_db.add_all(instances)
            self.session_db.commit()
        # TODO: change exceptions
        except Exception as e:
            self.report += f"{e} \n"
            return f"Some issues was occured: \n {self.report}"

        return f"All datas was completely loads: \n {self.report}"

    async def process(self):
        json_datas = await self.extract()
        models_instances = await self.transform(json_datas)
        result = await self.load(models_instances)
        return result
