import datetime
from decimal import Decimal

from pydantic import dataclasses
from pydantic.config import ConfigDict


@dataclasses.dataclass(config=ConfigDict(validate_assignment=True, orm_mode=True))
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
        instance_data = self.__dict__
        if '__pydantic_initialised__' in instance_data:
            del instance_data['__pydantic_initialised__']
        return instance_data
