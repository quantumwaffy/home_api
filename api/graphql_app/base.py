from functools import wraps
from typing import Any, Callable, Coroutine, Generic, Optional, TypeVar

import strawberry
from tortoise.queryset import QuerySet


@strawberry.type
class PageMeta:
    next_cursor: Optional[str] = strawberry.field(description="Next cursor")


T = TypeVar("T")


@strawberry.input
class FilterLookup(Generic[T]):
    gt: Optional[T] = None
    gte: Optional[T] = None
    lt: Optional[T] = None
    lte: Optional[T] = None
    contains: Optional[T] = None
    icontains: Optional[T] = None
    startswith: Optional[T] = None
    istartswith: Optional[T] = None
    endswith: Optional[T] = None
    iendswith: Optional[T] = None
    iexact: Optional[T] = None
    isnull: Optional[bool] = None
    not_isnull: Optional[bool] = None
    not_in: Optional[list[T]] = None
    _in: Optional[list[T]] = None
    search: Optional[str] = None
    range: Optional[list[T]] = None


@strawberry.input
class OrderLookup:
    desc: Optional[bool] = None
    asc: Optional[bool] = None

    def get_orm_lookup(self, field: str) -> Optional[str]:
        assert not all(self.__dict__.values()), f"Must be provided only one ordering type for '{field}'"
        prefix: str = "" if self.__dict__["asc"] else "-"
        return f"{prefix}{field}"


class Filter:
    def __call__(
        self, resolver
    ) -> Callable[[tuple[tuple[Any, ...], ...], dict[str, dict]], Coroutine[Any, Any, QuerySet]]:
        @wraps(resolver)
        async def wrapper(*args: tuple[Any, ...], **kwargs) -> QuerySet:
            resolver_qs: QuerySet = await resolver(*args, **kwargs)
            if _filter := kwargs["where"]:
                resolver_qs: QuerySet = resolver_qs.filter(**_filter.params)
            return resolver_qs

        return wrapper
