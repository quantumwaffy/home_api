import enum

from tortoise import fields, models


class TimeStamp(models.Model):
    created_at: fields.DatetimeField = fields.DatetimeField(auto_now_add=True)
    updated_at: fields.DatetimeField = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class EnumExtraMethodsMixin(enum.Enum):
    @classmethod
    @property
    def values(cls) -> tuple[str, ...]:
        return tuple(cls.__members__.values())
