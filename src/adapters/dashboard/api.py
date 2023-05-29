import logging.config


from fastapi import FastAPI

from application.ETL.dto import BookDTO
from application.ETL.services import ETL

info_logger = logging.getLogger('info_logger')


def configure_app(app: FastAPI, etl: ETL) -> None:

    @app.get('/dashboard', status_code=200, response_model=list[BookDTO])
    async def get_list():
        if await etl.process():
            info_logger.info('data was successfully uploaded!')
        else:
            info_logger.info('exceptions occurred!')
        return await etl.repository.get_all()
