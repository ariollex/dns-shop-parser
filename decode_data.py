async def get_price(soup):
    """
        Возвращает цену товара
    """
    return int(''.join([char for char in soup.find('div', class_='product-buy__price').text.strip() if char.isdigit()]))


async def get_availability(soup):
    """
        Возвращает количество магазинов, в которых можно приобрести товар. Если товар приобрести нельзя, возвращает 0.
    """
    if len(soup.find_all('div', class_='order-avail-wrap_not-avail')) != 0:
        return str(0)
    else:
        text = soup.find('div', class_='order-avail-wrap').text.strip()
        if 'наличии' in text:
            return str(''.join([char for char in text if char.isdigit()]))
        else:
            return 'на заказ'


async def get_group(soup):
    """
        Возвращает последнюю категорию товара.
    """
    return (soup.find_all('li', class_='breadcrumb-list__item initial-breadcrumb')[-1].find('span', itemprop='name')
            .text.strip())


async def get_characteristics(soup):
    """
        Возвращает характеристики товара.
    """
    specs_elements = soup.find_all('div', class_='product-characteristics__spec')

    # Создание словаря вида название_характеристики:характеристика
    characteristics_dict = {}
    for spec_element in specs_elements:
        title_element = spec_element.find('div', class_='product-characteristics__spec-title')
        value_element = spec_element.find('div', class_='product-characteristics__spec-value')

        if title_element and value_element:
            title = title_element.text.strip()
            value = value_element.text.strip()
            characteristics_dict[title] = value

    return characteristics_dict
