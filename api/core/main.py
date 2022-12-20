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

app = FastAPI()


@app.get("/")
async def root():
    return {"check_settings": settings.get_settings().dict()}


register_tortoise(
    app,
    config=database.TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
