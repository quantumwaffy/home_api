from base64 import b64decode, b64encode
from functools import wraps
from typing import Any, Callable, Coroutine, Optional, Type, TypeAlias, TypeVar, get_args

from tortoise.contrib.pydantic import PydanticModel
from tortoise.queryset import QuerySet

from . import metaclasses, mixins

Response = TypeVar("Response")
Resolver: TypeAlias = Callable[[tuple[tuple[Any, ...], ...], dict[str, dict]], Coroutine[Any, Any, Response]]


class CursorHandler:
    _codec: str = "ascii"
    _delimiter: str = ":"
    _unique_prefix_name: str = "UniqueName"

    def __init__(self, unique_prefix_name: Optional[str] = None, delimiter: Optional[str] = None) -> None:
        self._prefix: str = f"{unique_prefix_name or self._unique_prefix_name}{delimiter or self._delimiter}"

    def encode(self, obj_id: int) -> str:
        return b64encode(f"{self._prefix}{obj_id}".encode(self._codec)).decode(self._codec)

    def decode(self, unique_code: str) -> int:
        data: str = b64decode(unique_code.encode(self._codec)).decode(self._codec)
        return int(data.split(self._delimiter)[1])


class Paginator:
    _cursor_handler_class: "Type[CursorHandler]" = CursorHandler
    _pk_field_name: str = "id"

    def __init__(self, qs_schema: Optional["Type[PydanticModel]"] = None, pk_field_name: Optional[str] = None) -> None:
        self._qs_schema: "Type[PydanticModel]" = qs_schema
        if pk_field_name:
            self._pk_field_name = pk_field_name

    @staticmethod
    def _get_response_type(resolver: Resolver) -> "Type[Response]":
        response_type: "Type[Response]" = resolver.__annotations__["return"]
        assert issubclass(
            response_type, mixins.PageMixin
        ), f"{response_type.__name__} must be inherited from {mixins.PageMixin.__name__}"
        return response_type

    def _get_response_data(self, data: list[PydanticModel], cursor: Optional[str]):
        return self._response_type(
            **{
                self._response_type.data_field_name: data,
                self._response_type.page_meta: self._response_type.page_field_type(next_cursor=cursor),
            }
        )

    def _get_qs_schema(self) -> "Type[PydanticModel]":
        if not self._qs_schema:
            self._qs_schema: "Type[PydanticModel]" = get_args(
                self._response_type.__annotations__[self._response_type.data_field_name]
            )[0]._pydantic_type
        return self._qs_schema

    def __call__(self, resolver: Resolver) -> Response:
        self._response_type: "Type[Response]" = self._get_response_type(resolver)
        self._qs_schema: "Type[PydanticModel]" = self._get_qs_schema()

        @wraps(resolver)
        async def wrapper(*args: tuple[Any, ...], **kwargs) -> Response:
            resolver_qs: QuerySet = await resolver(*args, **kwargs)
            cursor_handler: CursorHandler = self._cursor_handler_class(resolver_qs.model.__class__.__name__)
            if not await resolver_qs.count():
                return self._get_response_data(await self._qs_schema.from_queryset(resolver_qs), None)
            return await self._get_paginated_data(
                resolver_qs, cursor_handler, kwargs["limit"], kwargs["cursor"], kwargs["order"]
            )

        return wrapper

    async def _get_paginated_data(
        self,
        data: QuerySet,
        cursor_handler: CursorHandler,
        limit: int,
        cursor: Optional[str],
        order: Optional[metaclasses.OrderClass],
    ) -> Response:

        if order and (order_params := order.params):
            data: QuerySet = data.order_by(*order_params)

        data_ids: list[int] = await data.values_list(self._pk_field_name, flat=True)

        first_obj_id_index: int = data_ids.index(cursor_handler.decode(cursor)) if cursor else 0

        last_obj_id_index: int = first_obj_id_index + limit

        try:
            last_obj_id: int = data_ids[last_obj_id_index]
        except IndexError:
            last_obj_id_index: int = len(data_ids)
            last_obj_id: int = data_ids[last_obj_id_index - 1]

        data: QuerySet = data.filter(**{f"{self._pk_field_name}__in": data_ids[first_obj_id_index:last_obj_id_index]})

        next_cursor: Optional[str] = cursor_handler.encode(last_obj_id) if data_ids[-1] != last_obj_id else None

        return self._get_response_data(await self._qs_schema.from_queryset(data), next_cursor)
