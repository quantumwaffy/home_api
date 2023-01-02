import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup, ResultSet, Tag
from core import utils as core_utils

from . import consts
from .models import BankCurrency


async def fetch_files(
    url: str, session: aiohttp.ClientSession, city: str, fields: tuple[str, ...], objects: list[BankCurrency]
):
    async with session.get(url + city) as response:
        return await parse_files(await response.read(), city, fields, objects)


async def parse_files(
    data: bytes, city: str, fields: tuple[str, ...], objects: list[BankCurrency]
) -> list[BankCurrency]:
    soup: BeautifulSoup = BeautifulSoup(data, "lxml")
    table_currency: Tag = soup.find("tbody", class_="sort_body")
    banks: ResultSet = table_currency.findAll(
        "tr",
        attrs={
            "data-currencies-courses-bank-id": re.compile(r".*"),
            "class": re.compile(r"^(?:c-currency-table__main-row|currencies-courses__row-main).*"),
        },
    )
    for bank in banks:
        bank_data: dict[str, str] = {"city_name": city}
        counter: int = 0
        for td in bank:
            if td.find("div"):
                continue
            if (bank_name_elem := td.find("a")) and not bank_name_elem.has_attr("class"):
                bank_data["bank_name"] = bank_name_elem.get_text()
                continue
            if bank_name_elem := td.find("img", class_="load_image"):
                bank_data["bank_name"] = bank_name_elem.get("alt")
                continue
            bank_data[fields[counter]] = currency_value.get_text() if (currency_value := td.find("span")) else None
            counter += 1
        objects.append(BankCurrency(**bank_data))
    return objects


async def get_currency_rate() -> int:
    async with aiohttp.ClientSession(headers={"User-agent": "currency bot 0.2"}) as session:
        objects: list[BankCurrency] = []
        fields: tuple[str, ...] = tuple(BankCurrency._meta.fields_map.keys())[5:]
        async with asyncio.TaskGroup() as tg:
            for city in consts.BelarusRegions.values:
                tg.create_task(fetch_files(consts.CURRENCY_SOURCE, session, city, fields, objects))
        if objects:
            await BankCurrency.all().delete()
            await core_utils.reset_table_sequence(BankCurrency._meta.db_table)
            created_objs: list[BankCurrency] = await BankCurrency.bulk_create(objects)
        return len(created_objs)
