from typing import Any, Optional, Type, TypeVar, get_args

from tortoise.contrib.pydantic import PydanticModel

from . import base

Filter = TypeVar("Filter")
TypeHint = TypeVar("TypeHint")


class FilterMeta(type):
    def __new__(
        mcs, name: str, bases: tuple[type, ...], attrs: dict, model: Optional[Type[PydanticModel]] = None
    ) -> "Type[Filter]":
        attrs |= {
            mcs.db_exp.__name__: mcs.db_exp,
            mcs._to_camel_case.__name__: staticmethod(mcs._to_camel_case),
            mcs._to_snake_case.__name__: staticmethod(mcs._to_snake_case),
        }
        filter_class: "Type[Filter]" = super().__new__(mcs, name, bases, attrs)

        if not model:
            return filter_class

        for field, typehint in model.__annotations__.items():
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

    def db_exp(self) -> dict[str, Any]:
        filled_filters: dict[str, Any] = {
            f"{self._to_snake_case(field)}__{lookup}": value
            for field, _filter in self.__dict__.items()
            if _filter
            for lookup, value in _filter.__dict__.items()
            if value
        }
        return filled_filters
