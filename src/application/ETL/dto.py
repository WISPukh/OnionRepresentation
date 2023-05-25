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
        if '__pydantic_initialised__' in instance:
            instance.pop('__pydantic_initialised__')
        return instance

    @classmethod
    def get_all(cls, data):
        return [cls.to_dict(book) for book in data]

    def to_dict(self) -> dict:
        return {
            field.description: getattr(self, field.description)
            for field in self.metadata.tables.get('Book').c
        }
