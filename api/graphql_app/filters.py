import strawberry
from news import schemas as news_schemas

from . import metaclasses


@strawberry.input
class BankCurrencyFilter(metaclass=metaclasses.FilterMeta, model=news_schemas.BankCurrencyView):
    ...
