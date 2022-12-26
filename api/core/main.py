from auth.router import router as auth_router
from core import database, settings
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

Tortoise.init_models(
    [
        "auth.models",
    ],
    "models",
)


def _init_app() -> FastAPI:
    api: FastAPI = FastAPI()
    api.include_router(auth_router)
    return api


app: FastAPI = _init_app()


@app.on_event("startup")
async def startup():
    register_tortoise(
        app,
        config=database.TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )


@app.get("/")
async def root():
    return {"check_settings": settings.get_settings().dict()}
