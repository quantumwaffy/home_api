from typing import Optional

import strawberry
from auth import models as auth_models
from auth import schemas as auth_schemas
from news import models as news_models
from news import schemas as news_schemas

from . import base, filters, mixins, pagination, permissions


@strawberry.experimental.pydantic.type(model=news_schemas.BankCurrencyView, all_fields=True)
class BankCurrencyViewType:
    ...


@strawberry.experimental.pydantic.type(model=auth_schemas.UserView, all_fields=True)
class UserViewType:
    ...


@strawberry.type
class BankCurrencyViewResponse(
    mixins.PageMixin,
    data_field_name="currencies",
    data_field_type=BankCurrencyViewType,
    data_field_params={"description": "The list of currencies"},
):
    ...


@strawberry.type
class UserViewResponse(
    mixins.PageMixin,
    data_field_name="users",
    data_field_type=UserViewType,
    data_field_params={"description": "The list of users"},
):
    ...


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[permissions.IsAuthenticated])
    @pagination.Paginator()
    @base.Filter()
    async def get_currency_rates(
        self,
        limit: int,
        cursor: Optional[str] = None,
        where: Optional[filters.BankCurrencyFilter] = None,
        order: Optional[filters.BankCurrencyOrder] = None,
    ) -> BankCurrencyViewResponse:
        return news_models.BankCurrency.all()

    @strawberry.field(permission_classes=[permissions.IsAuthenticated])
    @pagination.Paginator()
    @base.Filter()
    async def get_users(
        self,
        limit: int,
        cursor: Optional[str] = None,
        where: Optional[filters.UserFilter] = None,
        order: Optional[filters.UserOrder] = None,
    ) -> UserViewResponse:
        return auth_models.User.all()


schema: strawberry.Schema = strawberry.Schema(Query)
