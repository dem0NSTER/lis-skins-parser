import json
from _operator import itemgetter

import requests
from bs4 import BeautifulSoup


def read_json(path: str) -> dict:
    with open(path, encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_json(path: str, data) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_dollar() -> float:
    """This function can get course of dollar"""
    req = requests.get('https://www.banki.ru/products/currency/usd/').text
    soup = BeautifulSoup(req, 'lxml')
    dollar = float(soup.find(class_='Text__sc-j452t5-0 bCCQWi').text.split()[0].replace(',', '.'))
    return dollar


def del_data_file(file_nama: str) -> None:
    """This function can delete all data in file"""
    with open(file_nama, 'w', encoding='utf-8'):  # Write result to json
        pass


def rewrite_json(data: dict, dollar: float) -> dict:
    """This funciton rewrite json and add some strings in json and return list which include two json files:"""

    cant_find_items = []  # for item where i can find price in steam
    results = []

    for item in data:
        item_name = item['name']  # name of skin
        price = float(item['price'].replace('$', ''))  # price in dollars
        item_price = round(price * dollar, 2)  # price in RUB

        url = item['url']  # link for skin on lis-skins
        price_steam = item['price_steam']
        if price_steam == 0:  # if i cant find price in steam
            del item['price_steam']
            cant_find_items.append(item)
            write_json('D:/Python_program/scraping_lis_skins/json/cant_find.json', cant_find_items)
            continue

        profit = (price_steam - item_price) / item_price
        final_profit = round(profit, 4) * 100

        results.append(
            {
                "name": item_name,
                "price": item_price,
                "price_steam": price_steam,
                "profit": final_profit,
                "url": url
            }
        )
    return results


def save_results(data: dict) -> None:
    """This funciton sorted data and save all in final_results.json"""

    data = sorted(data, key=itemgetter('profit'), reverse=True)
    write_json('D:/Python_program/scraping_lis_skins/json/final_result.json', data)


if __name__ == '__main__':
    data = [
        {
            "name": "StatTrak™ AK-47 | Slate (Battle-Scarred)",
            "price": "6.57$",
            "discount": "-34%",
            "url": "https://lis-skins.ru/market/csgo/stattrak-ak-47-slate-battle-scarred/",
            "steam": "https://steamcommunity.com/market/listings/730/StatTrak™ AK-47 | Slate (Battle-Scarred)",
            "price_steam": 756.52
        },
        {
            "name": "Desert Eagle | Crimson Web (Well-Worn)",
            "price": "6.61$",
            "discount": "-34%",
            "url": "https://lis-skins.ru/market/csgo/desert-eagle-crimson-web-well-worn/",
            "steam": "https://steamcommunity.com/market/listings/730/Desert Eagle | Crimson Web (Well-Worn)",
            "price_steam": 0
        }
    ]

    dollar = get_dollar()
    results = rewrite_json(data, dollar)

    save_results(results)
