FROM python:3.13
LABEL authors="Cybernoobi"

WORKDIR /code

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

COPY . .

RUN if [ -f alembic.ini ]; then \
    alembic upgrade head; \
    fi
