import strawberry
from news import models as news_models
from news import schemas as news_schemas
from strawberry.types import Info


@strawberry.experimental.pydantic.type(model=news_schemas.BankCurrencyView, all_fields=True)
class BankCurrencyViewType:
    ...


@strawberry.type
class Query:
    @strawberry.field
    async def all_currency_rates(self, info: Info) -> list[BankCurrencyViewType]:
        return await news_schemas.BankCurrencyView.from_queryset(news_models.BankCurrency.all())


schema: strawberry.Schema = strawberry.Schema(Query)
