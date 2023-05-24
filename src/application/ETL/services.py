import json
from typing import Optional

from pydantic import dataclasses
from pydantic.error_wrappers import ValidationError
from application.interfaces import DB, SourceApi


class ETL:
    def __init__(
            self, db: DB, source_api: SourceApi, dto: dataclasses.dataclass
    ):
        self.db = db
        self.source_api = source_api
        self.dto = dto
        self.report: str = ""


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


    async def process(self):
        json_datas = await self.source_api.get()
        models_instances = await self.transform(json_datas)
        result = await self.db.save()
        return result



# EXTRACT
#         headers = {'Authorization': f'Bearer {self.auth_api}'}
#         url = self.source_api + f"?page_size={self.page_size}"
#
#         async with aiohttp.ClientSession() as session:
#             response = await session.get(url=url, headers=headers)
#             return await response.text()


# LOAD
#         try:
#             self.session_db.add_all(instances)
#             self.session_db.commit()
#         # TODO: change exceptions
#         except Exception as e:
#             self.report += f"{e} \n"
#             return f"Some issues was occured: \n {self.report}"
#
#         return f"All datas was completely loads: \n {self.report}"