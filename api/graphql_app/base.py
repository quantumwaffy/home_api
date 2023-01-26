from functools import wraps
from typing import Any, Callable, Coroutine, Generic, Optional, TypeVar

import strawberry
from tortoise.queryset import QuerySet

T = TypeVar("T")


@strawberry.input
class FilterLookup(Generic[T]):
    exact: Optional[T] = None
    gt: Optional[T] = None
    gte: Optional[T] = None
    lt: Optional[T] = None
    lte: Optional[T] = None
    contains: Optional[T] = None
    icontains: Optional[T] = None


class Filter:
    def __call__(
        self, resolver
    ) -> Callable[[tuple[tuple[Any, ...], ...], dict[str, dict]], Coroutine[Any, Any, QuerySet]]:
        @wraps(resolver)
        async def wrapper(*args: tuple[Any, ...], **kwargs) -> QuerySet:
            resolver_qs: QuerySet = await resolver(*args, **kwargs)
            return resolver_qs.filter(**kwargs["where"].filter_params)

        return wrapper
