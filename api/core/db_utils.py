from functools import wraps
from typing import Any, Callable, Coroutine, LiteralString

import asyncpg
from asyncpg import Connection


def connection(
    db_url: LiteralString,
) -> Callable[[Any], Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]]:
    def inner(func) -> Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            connect: Connection = await asyncpg.connect(db_url)
            func_result: Any = await func(connect, *args, **kwargs)
            await connect.close()
            return func_result

        return wrapper

    return inner
