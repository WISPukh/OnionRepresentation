from abc import ABC, abstractmethod
from typing import Sequence, Any


class BookRepository(ABC):

    @abstractmethod
    async def get_all(self) -> Sequence[Any]: ...

    @abstractmethod
    async def save(self, instances) -> bool: ...


class SourceApi(ABC):

    @abstractmethod
    async def get(self) -> str: ...
