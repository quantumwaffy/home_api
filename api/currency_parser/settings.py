from core import mixins as core_mixins
from pydantic import BaseSettings


class Settings(core_mixins.PSQLSettingsMixin, core_mixins.EnvConfigSettingsMixin, BaseSettings):
    BANK_CURRENCY_TABLE_NAME: str = "v1_news__bank_currency"


SETTINGS: Settings = Settings()
