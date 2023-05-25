import json

from aiohttp import ClientSession

from adapters.source_api.settings import settings
from application.interfaces import SourceApi as BaseSourceApi


class SourceApi(BaseSourceApi):
    def __init__(self, aiohttp_session: ClientSession, page_size: int, is_jwt: bool = True) -> None:
        self.base_url = settings.base_url
        self.aiohttp_session = aiohttp_session
        self.page_size = page_size
        self.is_jwt = is_jwt

    async def _get_access_token(self) -> str:
        token_url = f"{self.base_url}/token/"
        payload = {
            "email": settings.email,
            "password": settings.password
        }
        response = await self.aiohttp_session.post(token_url, json=payload)
        data_response = json.loads(await response.text())
        return data_response['access']

    async def get(self) -> str:
        headers = {"Authorization": f"Bearer {await self._get_access_token()}"} if self.is_jwt else dict()
        url = f"{self.base_url}/books/?page_size={self.page_size}"

        response = await self.aiohttp_session.get(url=url, headers=headers)
        return await response.text()
