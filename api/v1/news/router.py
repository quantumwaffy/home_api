from fastapi import APIRouter, Depends, status
from v1.auth import dependencies as auth_deps
from v1.auth import models as auth_models

from . import models, schemas
from .currency_parser import get_currency_rate

router: APIRouter = APIRouter(prefix="/news", tags=["news"])


@router.get("/currency/update-currency-rates", status_code=status.HTTP_201_CREATED)
async def update_currency_rate(user: auth_models.User = Depends(auth_deps.get_current_user)):  # noqa
    count_objs: int = await get_currency_rate()
    return {"updated_count": count_objs}


@router.get("/currency/list", response_model=list[schemas.BankCurrencyView])
async def currency_list(user: auth_models.User = Depends(auth_deps.get_current_user)):  # noqa
    return await schemas.BankCurrencyView.from_queryset(models.BankCurrency.all())
