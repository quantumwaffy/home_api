import datetime
from typing import Any

from asyncpg import Connection
from core.db_utils import connection
from core.settings import SETTINGS
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from . import exceptions, models, schemas


async def check_user_perms(user: models.User | None) -> None:
    if not user:
        raise exceptions.BaseAuthExceptionManager.no_user
    if user.disabled:
        raise exceptions.BaseAuthExceptionManager.blocked_user


async def get_user_from_token(token, key) -> models.User:
    try:
        payload: dict[str, Any] = jwt.decode(token, key, algorithms=[SETTINGS.JWT_ALGORITHM])
        jwt_payload: schemas.JWTPayload = schemas.JWTPayload(**payload)
        if jwt_payload.expiry_date < datetime.datetime.now():
            raise exceptions.BaseAuthExceptionManager.token_expired
    except (JWTError, ValidationError):
        raise exceptions.BaseAuthExceptionManager.credentials_error
    user: models.User = await models.User.filter(username=jwt_payload.username).first()
    await check_user_perms(user)
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
            algorithm=SETTINGS.JWT_ALGORITHM,
        )

    @classmethod
    async def create_jwt_tokens(cls, username: str, password: str) -> schemas.TokenGeneratedData:
        user: models.User | None = await models.User.filter(username=username).first()
        await check_user_perms(user)
        if not cls._verify_password(password, user.password_hash):
            raise exceptions.BaseAuthExceptionManager.authentication_error
        return schemas.TokenGeneratedData(
            access_token=cls._create_token(
                username, SETTINGS.JWT_ACCESS_TOKEN_EXPIRE_MIN, SETTINGS.JWT_ACCESS_TOKEN_SECRET_KEY
            ),
            refresh_token=cls._create_token(
                username, SETTINGS.JWT_REFRESH_TOKEN_EXPIRE_MIN, SETTINGS.JWT_REFRESH_TOKEN_SECRET_KEY
            ),
        )

    @classmethod
    async def get_refreshed_access_token(cls, refresh_token: str) -> str:
        user: models.User = await get_user_from_token(refresh_token, SETTINGS.JWT_REFRESH_TOKEN_SECRET_KEY)
        return cls._create_token(
            user.username, SETTINGS.JWT_ACCESS_TOKEN_EXPIRE_MIN, SETTINGS.JWT_ACCESS_TOKEN_SECRET_KEY
        )


@connection(SETTINGS.psql_url)
async def create_root_user(connect: Connection, table_name: str = models.User._meta.db_table) -> None:
    root_first_last_name: str = SETTINGS.SYS_ROOT_USERNAME.capitalize()
    await connect.execute(
        f"INSERT INTO {table_name} (username, first_name, last_name, password_hash) "
        f"values ('{SETTINGS.SYS_ROOT_USERNAME}','{root_first_last_name}',"
        f"'{root_first_last_name}','{Authenticator.get_password_hash(SETTINGS.SYS_ROOT_PASSWORD)}') "
        f"ON CONFLICT DO NOTHING;"
    )
