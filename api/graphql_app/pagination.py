from base64 import b64decode, b64encode
from functools import wraps
from typing import Any, Callable, Coroutine, Optional, Type

from tortoise.contrib.pydantic import PydanticModel
from tortoise.queryset import QuerySet

from . import filters, schemas


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

    def __init__(self, qs_schema: PydanticModel, pk_field_name: Optional[str] = None) -> None:
        self._qs_schema: PydanticModel = qs_schema
        if pk_field_name:
            self._pk_field_name = pk_field_name

    def __call__(
        self, resolver
    ) -> Callable[
        [tuple[tuple[Any, ...], ...], dict[str, dict]], Coroutine[Any, Any, "schemas.BankCurrencyViewResponse"]
    ]:
        @wraps(resolver)
        async def wrapper(*args: tuple[Any, ...], **kwargs) -> "schemas.BankCurrencyViewResponse":
            resolver_qs: QuerySet = await resolver(*args, **kwargs)
            self._cursor_handler: CursorHandler = self._cursor_handler_class(resolver_qs.model.__class__.__name__)
            if not await resolver_qs.count():
                return schemas.BankCurrencyViewResponse(
                    currencies=await self._qs_schema.from_queryset(resolver_qs),
                    page_meta=schemas.PageMeta(next_cursor=None),
                )
            return await self._get_paginated_data(resolver_qs, kwargs["limit"], kwargs["cursor"], kwargs["order"])

        return wrapper

    async def _get_paginated_data(
        self,
        data: QuerySet,
        limit: int,
        cursor: Optional[str] = None,
        order: Optional[filters.BankCurrencyOrder] = None,
    ) -> "schemas.BankCurrencyViewResponse":

        if order and (order_params := order.params):
            data: QuerySet = data.order_by(*order_params)

        data_ids: list[int] = await data.values_list(self._pk_field_name, flat=True)

        first_obj_id_index: int = data_ids.index(self._cursor_handler.decode(cursor)) if cursor else 0

        last_obj_id_index: int = first_obj_id_index + limit

        try:
            last_obj_id: int = data_ids[last_obj_id_index]
        except IndexError:
            last_obj_id_index: int = len(data_ids)
            last_obj_id: int = data_ids[last_obj_id_index - 1]

        data: QuerySet = data.filter(**{f"{self._pk_field_name}__in": data_ids[first_obj_id_index:last_obj_id_index]})

        next_cursor: Optional[str] = self._cursor_handler.encode(last_obj_id) if data_ids[-1] != last_obj_id else None

        return schemas.BankCurrencyViewResponse(
            currencies=await self._qs_schema.from_queryset(data),
            page_meta=schemas.PageMeta(next_cursor=next_cursor),
        )
