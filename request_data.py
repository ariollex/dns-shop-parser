from playwright.async_api import async_playwright
from time import sleep
import requests
import debug


async def get_cookies_list():
    """
        Возвращает Cookie, полученные с https://www.dns-shop.ru/.
    """
    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.dns-shop.ru/")
        try:
            await page.wait_for_selector('.homepage__container')
        except playwright._impl._errors.TimeoutError:
            return await get_cookies_list()
        cookies_list = await context.cookies()
        await browser.close()
    return cookies_list


def get_characteristics_url(url, cookies):
    """
        Возвращает URL на страницу с характеристиками
    """
    product_url = requests.get(url, cookies=cookies).url
    return product_url + 'characteristics/'


async def fetch_html_content(url, cookies):
    """
        Возвращает html страницу
    """
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        context = await browser.new_context()

        if cookies:
            await context.add_cookies(cookies)

        page = await context.new_page()
        await page.goto(url, timeout=0, wait_until='commit')
        try:
            await page.wait_for_selector('.product-buy__price')
            await page.wait_for_selector('div.order-avail-wrap')
        except Exception:  # Иногда dns-shop.ru почему-то перестаёт загружать .product-buy__price, так и не получив его.
            print(debug.w(), 'Не удалось получить .product-buy__price или .order-avail-wrap. Повторение попытки '
                             'через 10 секунд')
            sleep(10)
            return await fetch_html_content(url, cookies)

        # Получение контента страницы
        html_content = await page.content()

        await browser.close()
    return html_content
