# syntax=docker/dockerfile:1.2

FROM python:3.11-alpine

WORKDIR /api

RUN pip install poetry --root-user-action=ignore

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . .

CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
