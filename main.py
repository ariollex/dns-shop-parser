from request_data import get_cookies_list, get_characteristics_url, fetch_html_content
from decode_data import get_price, get_availability, get_group, get_characteristics

from bs4 import BeautifulSoup
from time import sleep
import asyncio
import random
import json

import debug


async def main():
    print(debug.i(), 'Чтение id...')
    # Чтение input.txt с id товаров
    file = open('input.txt')
    ids = []
    for i in file:
        if i != '\n':
            ids.append(str(int(i)))
    print(debug.i(), 'Все ID товаров:', *ids)

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
            product_id:
                {
                    "Цена": price,
                    "В наличии в магазинах": availability,
                    "Группа": group,
                    "Характеристики": characteristics
                }
        }

        # Чтение данных из существующего файла, если он существует
        existing_data = {}
        try:
            with open('output.json', 'r', encoding='utf-8') as json_file:
                existing_data = json.load(json_file)
        except FileNotFoundError:
            ...

        # Добавление новых данных
        existing_data.update(product_info)

        # Запись в json
        print(debug.i(), 'Запись информации товара с id', product_id, 'в json')
        with open('output.json', 'w', encoding='utf-8') as json_file:
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

        # Ожидание 4-8 сек во избежание тайм-аута
        sleep(random.randrange(start=4, stop=9))


if __name__ == "__main__":
    asyncio.run(main())
