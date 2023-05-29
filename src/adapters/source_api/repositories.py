import json
import logging
from typing import NoReturn, Literal

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError

from adapters.source_api.settings import settings
from application.interfaces import SourceApi as BaseSourceApi
from exceptions import RemoteServerError

ALLOWED_METHODS = Literal['GET', 'POST', 'PATCH', 'DELETE', 'PUT']


class SourceApi(BaseSourceApi):
    def __init__(self, page_size: int, is_jwt: bool = True) -> None:
        self.base_url = settings.base_url
        self.page_size = page_size
        self.is_jwt = is_jwt

    @staticmethod
    async def _make_request(
            url: str,
            method: ALLOWED_METHODS,
            /,
            payload: dict | None = None,
            headers: dict | None = None
    ) -> str | NoReturn:
        async with ClientSession(headers=headers) as session:
            session_method = getattr(session, method.lower())
            try:
                async with session_method(url=url, json=payload) as response:
                    return await response.text()
            except ClientConnectorError as exc:
                logging.error(exc)
                raise RemoteServerError('Exception from the upstream (external) server')

    async def _get_access_token(self) -> str:
        token_url = f"{self.base_url}/token/"
        payload = {
            "email": settings.email,
            "password": settings.password
        }
        tokens_str = await self._make_request(token_url, 'POST', payload=payload)
        token_data = json.loads(tokens_str)
        return token_data['access']

    async def get(self) -> str:
        headers = {"Authorization": f"Bearer {await self._get_access_token()}"} if self.is_jwt else None
        url = f"{self.base_url}/books/?page_size={self.page_size}"
        return await self._make_request(url, 'GET', headers=headers)
