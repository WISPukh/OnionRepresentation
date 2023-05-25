from fastapi import FastAPI

from application.ETL.dto import BookDTO
from application.ETL.services import ETL


def get_app(etl: ETL) -> FastAPI:
    async def get_list():
        if await etl.process():
            print('data was successfully uploaded!')
        else:
            print('exceptions occurred!')
        data = await etl.repository.get_all()
        return BookDTO.get_all(data)

    app = FastAPI()
    app.add_api_route('/dashboard', endpoint=get_list)
    return app
