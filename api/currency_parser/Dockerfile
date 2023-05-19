# syntax=docker/dockerfile:1.2

FROM python:3.11-alpine

WORKDIR /currency_parser

RUN pip install poetry --root-user-action=ignore

COPY ../currency_parser/poetry.lock ../currency_parser/pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

RUN mkdir core && touch core/__init__.py

COPY ../v1/news/models.py ./
COPY ../core/mixins.py ./core
COPY ../core/base.py ./core
COPY ../core/db_utils.py ./core
COPY ../core/metaclasses.py ./core

COPY ../currency_parser .

CMD ["python", "main.py"]