# syntax=docker/dockerfile:1

FROM python:3.10-alpine

ENV POETRY_VERSION=1.2.2 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --update-cache curl \
    && curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3 -

WORKDIR /src

COPY . .

RUN /root/.local/bin/poetry install --only main

CMD . /src/.venv/bin/activate && gunicorn -w 4 --bind=0.0.0.0:8080 'app:app'
