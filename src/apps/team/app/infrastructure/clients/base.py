from typing import Any
from abc import ABC, abstractmethod


class BaseClient(ABC):
    @abstractmethod
    async def get(self, url: str, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def post(self, url: str, data: Any = None, **kwargs: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
