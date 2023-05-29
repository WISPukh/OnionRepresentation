from fastapi import FastAPI

from application.ETL.dto import BookDTO
from application.ETL.services import ETL


def configure_app(app: FastAPI, etl: ETL) -> None:

    @app.get('/dashboard', status_code=200, response_model=list[BookDTO])
    async def get_list():
        if await etl.process():
            print('data was successfully uploaded!')
        else:
            print('exceptions occurred!')
        return await etl.repository.get_all()
