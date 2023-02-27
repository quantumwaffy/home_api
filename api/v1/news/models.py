from core import base as core_base
from core import mixins as core_mixins
from tortoise import fields


class BankCurrency(core_base.BaseModel, core_mixins.TimeStamp):
    bank_name = fields.CharField(max_length=255, null=True)
    city_name = fields.CharField(max_length=7, null=True)
    usd_buy = fields.DecimalField(max_digits=4, decimal_places=3, null=True)
    usd_sell = fields.DecimalField(max_digits=4, decimal_places=3, null=True)
    euro_buy = fields.DecimalField(max_digits=4, decimal_places=3, null=True)
    euro_sell = fields.DecimalField(max_digits=4, decimal_places=3, null=True)
    rub_buy = fields.DecimalField(max_digits=4, decimal_places=3, null=True)
    rub_sell = fields.DecimalField(max_digits=4, decimal_places=3, null=True)
    usd_buy_from_euro = fields.DecimalField(max_digits=5, decimal_places=3, null=True)
    usd_sell_from_euro = fields.DecimalField(max_digits=5, decimal_places=3, null=True)

    class Meta:
        table_description = "Bank actual currency info"
        unique_together = ("bank_name", "city_name")
        ordering = ["city_name", "bank_name"]

    def __str__(self) -> str:
        return f"{self.city_name}_{self.bank_name}"

    class PydanticMeta:
        exclude = ["created_at", "updated_at"]
