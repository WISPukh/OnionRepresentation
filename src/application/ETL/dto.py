from pydantic import dataclasses
import datetime
from decimal import Decimal
from pydantic.config import ConfigDict


@dataclasses.dataclass(config=ConfigDict(validate_assignment=True))
class BookDTO:
    id: int
    in_stock: int
    title: str
    description: str
    price: Decimal
    genres: list[int]
    author: list[int]
    release_date: datetime.date
    writing_date: datetime.date

    def dict_repr(self):
        instance = self.__dict__
        instance.pop('__pydantic_initialised__')
        return instance
