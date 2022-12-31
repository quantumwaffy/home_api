import enum

from core.mixins import EnumExtraMethodsMixin

CURRENCY_SOURCE: str = "https://myfin.by/currency/"


class BelarusCity(enum.StrEnum, EnumExtraMethodsMixin):
    MINSK = "minsk"
    BREST = "brest"
    VITEBSK = "vitebsk"
    GOMEL = "gomel"
    GRODNO = "grodno"
    MOGILEV = "mogilev"
