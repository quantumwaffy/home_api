from core import settings
from core.settings import Settings
from fastapi import Depends
from starlette.requests import Request

from . import models, schemas, utils

settings: Settings = settings.get_settings()


async def get_authenticated_user(request: Request) -> models.User:
    if (root_token := request.headers.get(settings.SECRET_HEADER_NAME)) and root_token == settings.SECRET_HEADER_VALUE:
        user: models.User = await models.User.get(username=settings.SYS_ROOT_USERNAME)
    else:
        token: str = await schemas.oauth2_scheme(request)
        user: models.User = await utils.get_user_from_token(token, settings.JWT_ACCESS_TOKEN_SECRET_KEY)
    return user


async def get_current_user(user: models.User = Depends(get_authenticated_user)) -> schemas.UserView:  # noqa
    return await schemas.UserView.from_tortoise_orm(user)
