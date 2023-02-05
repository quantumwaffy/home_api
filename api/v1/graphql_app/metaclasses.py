import abc
from typing import Any, Mapping, Optional, Type, TypeVar, get_args

from tortoise.contrib.pydantic import PydanticModel

from . import base

FilterClass = TypeVar("FilterClass")
OrderClass = TypeVar("OrderClass")
TypeHint = TypeVar("TypeHint")


class BaseResolverFuncMeta(abc.ABCMeta):
    _model_attr_name = "model"
    _choice_class_attr_name = "choice_class"

    @classmethod
    def __prepare__(mcs, name: str, bases: tuple[type, ...], **kwargs) -> Mapping[str, Any]:
        namespace: Mapping[str, Any] = super().__prepare__(name, bases)

        return namespace | {
            mcs.params.fget.__name__: mcs.params,
            mcs._to_camel_case.__name__: staticmethod(mcs._to_camel_case),
            mcs._to_snake_case.__name__: staticmethod(mcs._to_snake_case),
        }

    def __new__(
        mcs, name: str, bases: tuple[type, ...], attrs: dict, **kwargs: dict
    ) -> "Type[FilterClass | OrderClass]":
        mcs._model: Optional[Type[PydanticModel]] = kwargs.pop(mcs._model_attr_name, None)
        assert mcs._model, f"'{mcs._model_attr_name}' kwarg must be provided for class '{name}'"

        if custom_choice_class := kwargs.pop(mcs._choice_class_attr_name, None):
            mcs._choice_class = custom_choice_class
        return super().__new__(mcs, name, bases, attrs)

    @property
    @abc.abstractmethod
    def params(self) -> dict[str, Any]:
        ...

    @staticmethod
    def _to_camel_case(value: str) -> str:
        parts: list[str] = value.split("_")
        if len(parts) < 2:
            return value
        return parts[0] + "".join(part.title() for part in parts[1:])

    @staticmethod
    def _to_snake_case(value: str):
        def __format(char: str) -> str:
            if char.islower() or char == "_":
                return char
            return f"_{char.lower()}"

        return "".join(__format(char) for char in value)


class FilterMeta(BaseResolverFuncMeta):
    _choice_class = base.FilterLookup

    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict, **kwargs: dict) -> "Type[FilterClass]":
        filter_class: "Type[FilterClass]" = super().__new__(mcs, name, bases, attrs, **kwargs)
        for field, typehint in mcs._model.__annotations__.items():
            wrapped_typehints: tuple[TypeHint, ...] = get_args(typehint)
            camel_field: str = mcs._to_camel_case(field)
            filter_class.__annotations__ |= {
                camel_field: Optional[mcs._choice_class[wrapped_typehints[0] if wrapped_typehints else typehint]]
            }
            setattr(filter_class, camel_field, None)
        return filter_class

    @property
    def params(self) -> dict[str, Any]:
        return {
            f"{self._to_snake_case(field)}__{lookup.replace('_', '', 1) if lookup.startswith('_') else lookup}": value
            for field, _filter in self.__dict__.items()
            if _filter
            for lookup, value in _filter.__dict__.items()
            if value
        }


class OrderMeta(BaseResolverFuncMeta):
    _choice_class = base.OrderLookup

    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict, **kwargs: dict) -> "Type[OrderClass]":
        order_class: "Type[FilterClass]" = super().__new__(mcs, name, bases, attrs, **kwargs)

        for field in mcs._model.__annotations__:
            camel_field: str = mcs._to_camel_case(field)
            order_class.__annotations__ |= {camel_field: Optional[mcs._choice_class]}
            setattr(order_class, camel_field, None)
        return order_class

    @property
    def params(self) -> list[str]:
        return [
            lookup
            for field, order_obj in self.__dict__.items()
            if order_obj and (lookup := order_obj.get_orm_lookup(self._to_snake_case(field)))
        ]
