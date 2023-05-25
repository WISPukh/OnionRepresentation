import json

import aiohttp

from adapters.source_api.settings import settings
from application.interfaces import SourceApi as BaseSourceApi


class SourceApi(BaseSourceApi):
    def __init__(self, page_size: int, is_jwt: bool = True) -> None:
        self.base_url = settings.base_url
        self.page_size = page_size
        self.is_jwt = is_jwt

    async def _get_access_token(self) -> str:
        token_url = f"{self.base_url}/token/"
        payload = {
            "email": settings.email,
            "password": settings.password
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, json=payload) as response:
                data_response = json.loads(await response.text())
                return data_response['access']

    async def get(self) -> str:
        headers = {"Authorization": f"Bearer {await self._get_access_token()}"} if self.is_jwt else dict()
        url = f"{self.base_url}/books/?page_size={self.page_size}"
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url=url) as response:
                return await response.text()
