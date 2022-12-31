from typing import Type

from tortoise import fields
from tortoise.models import MetaInfo, Model, ModelMeta


class BaseMetaModel(ModelMeta):
    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict) -> "Type[Model]":
        model_class: "Type[Model]" = super().__new__(mcs, name, bases, attrs)
        if Model in bases:
            return model_class
        meta_attr: MetaInfo = model_class._meta
        if not meta_attr.db_table:
            meta_attr.db_table = "_".join((model_class.app_name, mcs._get_name_postfix(name)))

        attrs.update(id=fields.IntField(pk=True))
        return model_class

    @staticmethod
    def _get_name_postfix(name: str) -> str:
        def __format_func(char: str) -> str:
            if char.isdigit() or char.islower():
                return char
            return f"_{char.lower()}"

        return "".join(map(__format_func, name))
