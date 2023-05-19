from core import mixins
from pydantic import BaseSettings


class Settings(mixins.PSQLSettingsMixin, mixins.EnvConfigSettingsMixin, BaseSettings):
    DEBUG: bool
    JWT_ACCESS_TOKEN_SECRET_KEY: str
    JWT_REFRESH_TOKEN_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MIN: int
    JWT_REFRESH_TOKEN_EXPIRE_MIN: int
    SYS_ROOT_USERNAME: str
    SYS_ROOT_PASSWORD: str
    SECRET_HEADER_NAME: str
    SECRET_HEADER_VALUE: str
    CURRENCY_UPDATE_DELTA_SEC: int


SETTINGS: Settings = Settings()
