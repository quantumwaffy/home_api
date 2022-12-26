import datetime
from typing import Any

from core import settings
from core.settings import Settings
from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import models
from .exceptions import authentication_error, credentials_error
from .schemas import TokenData, User_Pydantic, oauth2_scheme

settings: Settings = settings.get_settings()


class Authenticator:
    _pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    async def _verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def get_password_hash(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    @staticmethod
    async def _get_db_user(username: str) -> models.User | None:
        return await models.User.filter(username=username).first()

    @classmethod
    async def create_access_token(cls, username: str, password: str) -> str:
        user: models.User | None = await cls._get_db_user(username)
        if not user or not cls._verify_password(password, user.password_hash):
            raise authentication_error
        expire: datetime.datetime = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MIN
        )
        return jwt.encode(
            {"username": username, "expire": expire}, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)):  # noqa
        try:
            payload: dict[str, Any] = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            username: str = payload.get("username")
            if not username:
                raise credentials_error
            token_data: TokenData = TokenData(username=username)
        except JWTError:
            raise credentials_error
        user: models.User = await cls._get_db_user(token_data.username)
        if not user:
            raise credentials_error
        return User_Pydantic.from_queryset_single(user)
