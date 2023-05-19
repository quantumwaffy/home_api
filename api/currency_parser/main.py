import asyncio
from parser import update_currency_rates
from typing import Any

from settings import SETTINGS
from tortoise import Tortoise


async def main():
    await Tortoise.init(db_url=SETTINGS.psql_url, modules={"models": ("models",)})
    return await update_currency_rates()


def handler(event: dict[str, Any] | None = None, context: dict[str, Any] | None = None) -> None:
    asyncio.run(main())


if __name__ == "__main__":
    handler()
