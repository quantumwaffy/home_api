from typing import Generic, Optional, TypeVar

import strawberry

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
