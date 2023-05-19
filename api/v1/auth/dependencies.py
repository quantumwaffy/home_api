from core.settings import SETTINGS
from fastapi import Depends
from starlette.requests import Request

from . import models, schemas, utils


async def get_authenticated_user(request: Request) -> models.User:
    if (root_token := request.headers.get(SETTINGS.SECRET_HEADER_NAME)) and root_token == SETTINGS.SECRET_HEADER_VALUE:
        user: models.User = await models.User.get(username=SETTINGS.SYS_ROOT_USERNAME)
    else:
        token: str = await schemas.oauth2_scheme(request)
        user: models.User = await utils.get_user_from_token(token, SETTINGS.JWT_ACCESS_TOKEN_SECRET_KEY)
    return user


async def get_current_user(user: models.User = Depends(get_authenticated_user)) -> schemas.UserDB:  # noqa
    return await schemas.UserDB.from_tortoise_orm(user)
