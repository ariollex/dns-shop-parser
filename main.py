from request_data import get_cookies_list, get_characteristics_url, fetch_html_content
from decode_data import get_price, get_availability, get_group, get_characteristics
from utils.json_utils import json_write

from bs4 import BeautifulSoup
from time import sleep
import asyncio
import random

import debug


async def main():
    print(debug.i(), 'чтение id...')
    # Чтение input.txt с id товаров
    file = open('input.txt')
    ids = []
    for i in file:
        if i != '\n':
            ids.append(str(int(i)))

    # Получение куки
    cookies_list = await get_cookies_list()
    cookies = {}
    for c in cookies_list:
        cookies.update({c["name"]: c["value"]})

    for product_id in ids:
        # Получение html с полными характеристиками
        print(debug.i(), 'Получение html страницы товара с id:', product_id)
        html_content = await fetch_html_content(url=get_characteristics_url('https://dns-shop.ru/search/?q=' +
                                                                            product_id, cookies), cookies=cookies_list)
        soup = BeautifulSoup(html_content, 'html.parser')

        # Получение характеристик
        print(debug.i(), 'Получение характеристик товара с id:', product_id)
        price = await get_price(soup)
        availability = await get_availability(soup)
        group = await get_group(soup)
        characteristics = await get_characteristics(soup)

        # Словарь с характеристиками товара
        product_info = {
            "Цена": price,
            "В наличии в магазинах": availability,
            "Группа": group,
            "Характеристики": characteristics
        }

        # Запись в json
        print(debug.i(), 'Запись информации товара с id', product_id, 'в json')
        json_write(product_id=product_id, product_info=product_info)

        # Ожидание 4-6 сек во избежание тайм-аута
        sleep(random.randrange(start=4, stop=7))

if __name__ == "__main__":
    asyncio.run(main())
