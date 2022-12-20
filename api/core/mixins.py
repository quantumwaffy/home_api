from tortoise import fields, models


class TimeStamp(models.Model):
    created_at: fields.DatetimeField = fields.DatetimeField(auto_now_add=True)
    updated_at: fields.DatetimeField = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
