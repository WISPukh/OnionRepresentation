import logging

import uvicorn
from fastapi import FastAPI

from adapters.dashboard.api import dashboard

logging.basicConfig(
    format='%(pathname)s\n%(asctime)s LINE NUMBER - %(lineno)d: FUNCTION - %(funcName)s \n %(message)s\n',
    datefmt='(%I:%M:%S %p)',
    filename='errors.log',
    encoding='utf-8',
    level=logging.ERROR
)
logger = logging.Logger('main_logger')

app = FastAPI()
app.include_router(dashboard)


@app.get("/")
async def root():
    return {"message": "Server is running!"}


if __name__ == '__main__':
    uvicorn.run(app)
