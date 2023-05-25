from sqlalchemy import Integer, String, Date, Column, Text, ARRAY
from composites.database.postgres_db import Base


class Book(Base):
    __tablename__ = 'Book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    in_stock = Column(Integer, default=0, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    genres = Column(ARRAY(Integer))
    author = Column(ARRAY(Integer))
    release_date = Column(Date)
    writing_date = Column(Date)
