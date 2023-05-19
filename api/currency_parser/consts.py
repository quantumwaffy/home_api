import enum

from core import mixins as core_mixins

CURRENCY_SOURCE: str = "https://myfin.by/currency/"


class BelarusRegions(enum.StrEnum, core_mixins.EnumExtraMethodsMixin):
    MINSK = "minsk"
    BREST = "brest"
    VITEBSK = "vitebsk"
    GOMEL = "gomel"
    GRODNO = "grodno"
    MOGILEV = "mogilev"
