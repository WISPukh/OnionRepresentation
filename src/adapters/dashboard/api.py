from fastapi import APIRouter, Depends

from application.ETL.dto import BookDTO
from application.ETL.services import ETL
from application.interfaces import BookRepository
from composites.utils import get_db, get_etl

dashboard = APIRouter(prefix='/dashboard', tags=['dashboard'])


@dashboard.get('/', response_model=None, status_code=200)
async def get_list(db: BookRepository = Depends(get_db), etl: ETL = Depends(get_etl)):

    if await etl.process():
        print('data was successfully uploaded!')
    else:
        print('exceptions occurred!')
    return BookDTO.get_all(await db.get_all())
