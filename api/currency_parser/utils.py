from asyncpg import Connection
from core import db_utils as core_db_utils
from settings import SETTINGS


@core_db_utils.connection(SETTINGS.psql_url)
async def reset_table_sequence(connect: Connection, table_name: str, pr_key_name: str = "id") -> None:
    await connect.execute(
        f"SELECT setval('{table_name}_{pr_key_name}_seq', 1);" f"UPDATE {table_name} SET {pr_key_name} = DEFAULT;"
    )
