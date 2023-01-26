from typing import Any, Mapping, Optional, Type, TypeVar, get_args

from tortoise.contrib.pydantic import PydanticModel

from . import base

FilterClass = TypeVar("FilterClass")
TypeHint = TypeVar("TypeHint")


class FilterMeta(type):
    _lookup_class = base.FilterLookup

    @classmethod
    def __prepare__(mcs, name: str, bases: tuple[type, ...], **kwargs) -> Mapping[str, Any]:
        namespace: Mapping[str, Any] = super().__prepare__(name, bases)

        return namespace | {
            mcs.filter_params.fget.__name__: mcs.filter_params,
            mcs._to_camel_case.__name__: staticmethod(mcs._to_camel_case),
            mcs._to_snake_case.__name__: staticmethod(mcs._to_snake_case),
        }

    def __new__(mcs, name: str, bases: tuple[type, ...], attrs: dict, **kwargs: dict) -> "Type[FilterClass]":
        mcs._model: Optional[Type[PydanticModel]] = kwargs.pop("model", None)

        if custom_lookup_class := kwargs.pop("lookup_class", None):
            mcs._lookup_class = custom_lookup_class

        filter_class: "Type[FilterClass]" = super().__new__(mcs, name, bases, attrs)

        if not mcs._model:
            return filter_class

        for field, typehint in mcs._model.__annotations__.items():
            wrapped_typehints: tuple[TypeHint, ...] = get_args(typehint)
            camel_field: str = mcs._to_camel_case(field)
            filter_class.__annotations__ |= {
                camel_field: Optional[base.FilterLookup[wrapped_typehints[0] if wrapped_typehints else Any]]
            }
            setattr(filter_class, camel_field, None)
        return filter_class

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

    @property
    def filter_params(self) -> dict[str, Any]:
        filled_filters: dict[str, Any] = {
            f"{self._to_snake_case(field)}__{lookup}": value
            for field, _filter in self.__dict__.items()
            if _filter
            for lookup, value in _filter.__dict__.items()
            if value
        }
        return filled_filters
