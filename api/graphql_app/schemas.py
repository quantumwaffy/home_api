from typing import List, Optional

import strawberry
from news import models as news_models
from news import schemas as news_schemas

from . import filters, pagination, permissions


@strawberry.type
class PageMeta:
    next_cursor: Optional[str] = strawberry.field(description="Next cursor")


@strawberry.experimental.pydantic.type(model=news_schemas.BankCurrencyView, all_fields=True)
class BankCurrencyViewType:
    ...


@strawberry.type
class BankCurrencyViewResponse:
    currencies: List[BankCurrencyViewType] = strawberry.field(description="The list of currencies")
    page_meta: PageMeta = strawberry.field(description="Pagination metadata")


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[permissions.IsAuthenticated])
    @pagination.Paginator(qs_schema=news_schemas.BankCurrencyView)
    async def get_currency_rates(
        self, limit: int, cursor: Optional[str] = None, where: Optional[filters.Filter] = None
    ) -> BankCurrencyViewResponse:
        print(where.db_exp())
        return news_models.BankCurrency.all()


schema: strawberry.Schema = strawberry.Schema(Query)
