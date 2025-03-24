from httpx import AsyncClient, Response
from typing import Any, override

from app.infrastructure.clients.base import BaseClient


class HTTPXClient(BaseClient):
    def __init__(self, client: AsyncClient) -> None:
        self._client = client

    @override
    async def get(self, url: str, **kwargs: Any) -> Response:
        return await self._client.get(url, **kwargs)

    @override
    async def post(self, url: str, data: Any = None, **kwargs: Any) -> Response:
        return await self._client.post(url, data=data, **kwargs)

    @override
    async def close(self) -> None:
        await self._client.aclose()
