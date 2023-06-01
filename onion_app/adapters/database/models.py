from sqlalchemy import Integer, String, Date, Column, Text, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()


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
