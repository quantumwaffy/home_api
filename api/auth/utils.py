import datetime
from typing import Any

from core import settings
from core.settings import Settings
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from . import exceptions, models, schemas

settings: Settings = settings.get_settings()


async def get_user_from_token(token, key) -> models.User:
    try:
        payload: dict[str, Any] = jwt.decode(token, key, algorithms=[settings.JWT_ALGORITHM])
        jwt_payload: schemas.JWTPayload = schemas.JWTPayload(**payload)
        if jwt_payload.expiry_date < datetime.datetime.now():
            raise exceptions.access_token_expired
    except (JWTError, ValidationError):
        raise exceptions.credentials_error
    user: models.User = await models.User.filter(username=jwt_payload.username).first()
    if not user:
        raise exceptions.no_user
    return user


class Authenticator:
    _pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def _verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls._pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls._pwd_context.hash(password)

    @staticmethod
    def _create_token(subject: str, expiry_delta: int, key: str) -> str:
        expiry_dt: datetime.datetime = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_delta)
        return jwt.encode(
            {"sub": subject, "exp": expiry_dt},
            key,
            algorithm=settings.JWT_ALGORITHM,
        )

    @classmethod
    async def create_jwt_tokens(cls, username: str, password: str) -> schemas.TokenGeneratedData:
        user: models.User | None = await models.User.filter(username=username).first()
        if not user:
            raise exceptions.no_user
        if not cls._verify_password(password, user.password_hash):
            raise exceptions.authentication_error
        return schemas.TokenGeneratedData(
            access_token=cls._create_token(
                username, settings.JWT_ACCESS_TOKEN_EXPIRE_MIN, settings.JWT_ACCESS_TOKEN_SECRET_KEY
            ),
            refresh_token=cls._create_token(
                username, settings.JWT_REFRESH_TOKEN_EXPIRE_MIN, settings.JWT_REFRESH_TOKEN_SECRET_KEY
            ),
        )

    @classmethod
    async def get_refreshed_access_token(cls, refresh_token: str) -> str:
        user: models.User = await get_user_from_token(refresh_token, settings.JWT_REFRESH_TOKEN_SECRET_KEY)
        return cls._create_token(
            user.username, settings.JWT_ACCESS_TOKEN_EXPIRE_MIN, settings.JWT_ACCESS_TOKEN_SECRET_KEY
        )
