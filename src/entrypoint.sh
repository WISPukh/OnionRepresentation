#!/bin/sh

alembic upgrade head
uvicorn --port ${SERVER_PORT} --host 0.0.0.0 --loop asyncio --reload composites.app:app
