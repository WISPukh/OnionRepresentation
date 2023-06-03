FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /src

COPY /onion_app /src/onion_app
COPY /onion_app/setup.cfg /src/onion_app
COPY /onion_app/pyproject.toml /src/onion_app
COPY /deployment/entrypoint.sh /src

WORKDIR /src

RUN pip install --no-cache-dir onion_app/.
#
ENV PYTHONPATH "${PYTHONPATH}:/src"

EXPOSE ${SERVER_PORT}
