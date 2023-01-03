from auth.router import router as auth_router
from core import database, settings
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from graphql_app.router import router as graphql_router
from news.currency_parser import get_currency_rate
from news.router import router as news_router
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from . import utils

Tortoise.init_models(
    ["auth.models", "news.models"],
    "models",
)


def _init_app() -> FastAPI:
    api: FastAPI = FastAPI()
    api.include_router(auth_router)
    api.include_router(news_router)
    api.include_router(graphql_router)
    return api


app: FastAPI = _init_app()


@app.on_event("startup")
async def startup():
    register_tortoise(
        app,
        config=database.TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )


@app.on_event("startup")
async def create_init_db_data():
    await utils.create_root_user()


@app.get("/")
async def root():
    return {"check_settings": settings.get_settings().dict()}


@app.on_event("startup")
@repeat_every(seconds=1800)
async def update_currency_rates():
    await get_currency_rate()
