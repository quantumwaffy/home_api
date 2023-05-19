from fastapi import APIRouter, Depends
from v1.auth import dependencies as auth_deps
from v1.auth import models as auth_models

from . import models, schemas

router: APIRouter = APIRouter(prefix="/news", tags=["news"])


@router.get("/currency/list", response_model=list[schemas.BankCurrencyView])
async def currency_list(user: auth_models.User = Depends(auth_deps.get_current_user)):  # noqa
    return await schemas.BankCurrencyView.from_queryset(models.BankCurrency.all())
