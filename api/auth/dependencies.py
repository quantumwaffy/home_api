from core import settings
from core.settings import Settings
from fastapi import Depends

from . import models, schemas, utils

settings: Settings = settings.get_settings()


async def get_current_user(token: str = Depends(schemas.oauth2_scheme)):  # noqa
    user: models.User = await utils.get_user_from_token(token, settings.JWT_ACCESS_TOKEN_SECRET_KEY)
    return await schemas.UserView.from_tortoise_orm(user)
