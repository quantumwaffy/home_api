import strawberry
from v1.auth import schemas as auth_schemas
from v1.news import schemas as news_schemas

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
