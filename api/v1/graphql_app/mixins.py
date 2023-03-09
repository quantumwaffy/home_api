from typing import Any, List, Optional, TypeVar

import strawberry
from v1.auth import models as auth_models
from v1.auth.dependencies import get_authenticated_user

from . import base

DataType = TypeVar("DataType")


class ContextUserMixin:
    @staticmethod
    async def _get_user(context: dict[str, Any]) -> auth_models.User:
        user: auth_models.User | None = await get_authenticated_user(context["request"])
        context["user"] = user
        return user


class PageMixin:
    __data_field_name_kwarg: str = "data_field_name"
    __data_field_type_kwarg: str = "data_field_type"
    __data_field_params_kwarg: str = "data_field_params"

    __page_field_name: str = "page_meta"
    __page_field_params_kwarg: str = "page_field_params"
    __page_type_attr_name: str = "page_field_type"
    _page_field_type: base.PageMeta = base.PageMeta

    def __init_subclass__(cls, **kwargs) -> None:
        data_field: Optional[str] = kwargs.pop(cls.__data_field_name_kwarg, None)
        assert data_field, f"Kwarg '{cls.__data_field_name_kwarg}' must be provided for '{cls.__name__}'"

        type_field: Optional[DataType] = kwargs.pop(cls.__data_field_type_kwarg, None)
        assert type_field, f"Kwarg '{cls.__data_field_type_kwarg}' must be provided for '{cls.__name__}'"

        cls.__annotations__ |= {data_field: List[type_field], cls.__page_field_name: cls._page_field_type}

        setattr(cls, data_field, strawberry.field(**kwargs.pop(cls.__data_field_params_kwarg, {})))
        setattr(
            cls,
            cls.__page_field_name,
            strawberry.field(description="Pagination metadata", **kwargs.pop(cls.__page_field_params_kwarg, {})),
        )

        setattr(cls, cls.__data_field_name_kwarg, data_field)
        setattr(cls, cls.__page_field_name, cls.__page_field_name)
        setattr(cls, cls.__page_type_attr_name, cls._page_field_type)

        super().__init_subclass__(**kwargs)
