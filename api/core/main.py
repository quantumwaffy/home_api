from core import database
from core.settings import SETTINGS
from fastapi import FastAPI
from mangum import Mangum
from tortoise.contrib.fastapi import register_tortoise
from v1.auth.utils import create_root_user

from . import routers


def _init_app() -> FastAPI:
    api: FastAPI = FastAPI(
        debug=SETTINGS.DEBUG,
        swagger_ui_parameters={"persistAuthorization": True},
        **{"docs_url": None, "redoc_url": None} if not SETTINGS.DEBUG else {}
    )
    for prefix, routs in routers.AppRouter.routers:
        [api.include_router(router, prefix=prefix) for router in routs]
    register_tortoise(
        api,
        config=database.TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    return api


app: FastAPI = _init_app()

handler: Mangum = Mangum(app)


@app.on_event("startup")
async def create_init_db_data():
    await create_root_user()
