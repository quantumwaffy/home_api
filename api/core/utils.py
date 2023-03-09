from functools import wraps
from typing import Any, Callable, Coroutine

import asyncpg
from asyncpg import Connection
from core.settings import Settings, get_settings

settings: Settings = get_settings()


def connection(func) -> Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        connect: Connection = await asyncpg.connect(settings.get_psql_url())
        func_result: Any = await func(connect, *args, **kwargs)
        await connect.close()
        return func_result

    return wrapper


@connection
async def reset_table_sequence(connect: Connection, table_name: str, pr_key_name: str = "id") -> None:
    await connect.execute(
        f"SELECT setval('{table_name}_{pr_key_name}_seq', 1);" f"UPDATE {table_name} SET {pr_key_name} = DEFAULT;"
    )
