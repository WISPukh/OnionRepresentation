from abc import ABC, abstractmethod
from typing import Sequence, Any


class BookRepository(ABC):

    @abstractmethod
    async def get_all(self) -> Sequence[Any]: ...
