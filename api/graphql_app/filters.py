import strawberry
from auth import schemas as auth_schemas
from news import schemas as news_schemas

from . import metaclasses


@strawberry.input
class BankCurrencyFilter(metaclass=metaclasses.FilterMeta, model=news_schemas.BankCurrencyView):
    ...


@strawberry.input
class BankCurrencyOrder(metaclass=metaclasses.OrderMeta, model=news_schemas.BankCurrencyView):
    ...


@strawberry.input
class UserFilter(metaclass=metaclasses.FilterMeta, model=auth_schemas.UserView):
    ...


@strawberry.input
class UserOrder(metaclass=metaclasses.OrderMeta, model=auth_schemas.UserView):
    ...
