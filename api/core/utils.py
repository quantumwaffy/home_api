from functools import wraps
from typing import Any, Callable, Coroutine

import asyncpg
from asyncpg import Connection
from auth.utils import Authenticator
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
async def create_root_user(connect: Connection) -> None:
    root_first_last_name: str = settings.SYS_ROOT_USERNAME.capitalize()
    await connect.execute(
        f"INSERT INTO auth__user (username, first_name, last_name, password_hash) "
        f"values ('{settings.SYS_ROOT_USERNAME}','{root_first_last_name}',"
        f"'{root_first_last_name}','{Authenticator.get_password_hash(settings.SYS_ROOT_PASSWORD)}') "
        f"ON CONFLICT DO NOTHING;"
    )


@connection
async def reset_table_sequence(connect: Connection, table_name: str, pr_key_name: str = "id") -> None:
    await connect.execute(
        f"SELECT setval('{table_name}_{pr_key_name}_seq', 1);" f"UPDATE {table_name} SET {pr_key_name} = DEFAULT;"
    )
