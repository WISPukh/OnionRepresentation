from abc import ABC, abstractmethod


class BookRepository(ABC):

    @abstractmethod
    async def save(self, instances) -> bool: ...


class SourceApi(ABC):

    @abstractmethod
    async def get(self) -> str: ...
