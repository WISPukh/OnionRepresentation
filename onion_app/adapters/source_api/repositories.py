import json
import logging
from typing import NoReturn, Optional, Union

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorError

from onion_app.application.ETL import interfaces
from onion_app.application.exceptions import RemoteServerError
from .constatns import ALLOWED_METHODS


class SourceApi(interfaces.SourceApi):
    def __init__(
        self,
        page_size: int,
        base_url: str,
        email: str,
        password: str,
        is_jwt: bool = True,
    ) -> None:
        self._base_url = base_url
        self._page_size = page_size
        self._is_jwt = is_jwt
        self._email = email
        self._password = password

    @staticmethod
    async def _make_request(
        url: str,
        method: ALLOWED_METHODS,
        *,
        payload: Optional[dict] = None,
        headers: Optional[dict] = None
    ) -> Union[str, NoReturn]:
        async with ClientSession(headers=headers) as session:
            session_method = getattr(session, method.lower())
            try:
                async with session_method(url=url, json=payload) as response:
                    return await response.text()
            except ClientConnectorError as exc:
                logging.error(exc)
                raise RemoteServerError('Exception from the upstream (external) server')

    async def _get_access_token(self) -> str:
        token_url = f"{self._base_url}/token/"
        payload = {
            "email": self._email,
            "password": self._password
        }
        tokens_str = await self._make_request(token_url, 'POST', payload=payload)
        token_data = json.loads(tokens_str)
        return token_data['access']

    async def get(self) -> str:  # TODO: change to get_books
        headers = {"Authorization": f"Bearer {await self._get_access_token()}"} if self._is_jwt else None
        url = f"{self._base_url}/books/?page_size={self._page_size}"
        return await self._make_request(url, 'GET', headers=headers)
