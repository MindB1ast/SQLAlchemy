#RUN pip install --no-cache-dir --upgrade gunicorn uvicorn sqlalchemy alembic fastapi
FROM python:3.10

LABEL maintainer="lialia2000@inbox.ru"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./src /code/src
COPY ./alembic.ini /code/alembic.ini
COPY ./migrations /code/migrations

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt