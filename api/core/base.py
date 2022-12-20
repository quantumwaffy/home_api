from core import metaclasses
from tortoise import models


class BaseModel(models.Model, metaclass=metaclasses.BaseMetaModel):
    def __init_subclass__(cls, **kwargs):
        cls.app_name = cls.__module__.split(".")[0]
        return super().__init_subclass__()
