import logging.config

from fastapi import FastAPI

from onion_app.application import interfaces
from onion_app.application.dto import BookDTO

info_logger = logging.getLogger('info_logger')


def configure_app(app: FastAPI, book_repo: interfaces.BookRepository) -> None:

    @app.get('/dashboard', status_code=200, response_model=list[BookDTO])
    async def get_list():
        return await book_repo.get_all()

    @app.get('/')
    async def root():
        return {"message": "Server is running!"}
