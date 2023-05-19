import enum

from pydantic import BaseSettings
from tortoise import fields, models


class TimeStamp(models.Model):
    created_at: fields.DatetimeField = fields.DatetimeField(auto_now_add=True)
    updated_at: fields.DatetimeField = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class EnumExtraMethodsMixin(enum.Enum):
    @classmethod
    @property
    def values(cls) -> tuple[str, ...]:
        return tuple(cls.__members__.values())


class EnvConfigSettingsMixin(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


class PSQLSettingsMixin(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    @property
    def psql_url(self) -> str:
        return (
            f"postgres://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
