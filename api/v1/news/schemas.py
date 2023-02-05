from tortoise.contrib.pydantic import pydantic_model_creator

from . import models

BankCurrencyView = pydantic_model_creator(models.BankCurrency, name="BankCurrencyView", exclude_readonly=True)
