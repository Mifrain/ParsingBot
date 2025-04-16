from collections import defaultdict

import aiohttp
from lxml import html
from typing import List
import ssl
import certifi
import re


from bot.db.models import Site
from bot.db.services import SiteService


async def clean_price(price_str: str) -> float:
    price_str = price_str.replace(',', '.')
    cleaned = re.findall(r'\d+\.?\d*', price_str.replace(' ', ''))
    return float(cleaned[0]) if cleaned else 0.0



async def parse_price(site_id: int, url: str, xpath):
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_context)) as session:
            async with session.get(url) as response:

                response.raise_for_status()
                tree = html.fromstring(await response.text())
                price_element = tree.xpath(xpath)

                if price_element:
                    price_text = price_element[0].text_content().strip()
                    price = await clean_price(price_text)

                    SiteService.update_price(site_id, price)
                else:
                    print(f"Цена не найдена для {url} по XPath: {xpath}")
                    return None
    except Exception as e:
        print(f"Ошибка при парсинге сайта {url}: {e}")
        return None


async def get_summarize():
    new_sites: List[Site] = SiteService.get_sites_without_price()

    for site in new_sites:
        await parse_price(site[0].id, site[0].url, site[0].xpath)

    all_prices = SiteService.get_all_sites()

    grouped_prices = defaultdict(list)


    for site in all_prices:
        if site[1] < 1: continue
        title = site[0].strip()
        price = site[1]
        grouped_prices[title].append(price)

    text="Сводка по товарам:\n"
    text += "\n".join(f"{title}: { sum(prices) / len(prices):.2f}" for title, prices in grouped_prices.items())

    return text