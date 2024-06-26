import json
from _operator import itemgetter

import requests
from bs4 import BeautifulSoup


def get_dollar() -> float:
    req = requests.get('https://www.banki.ru/products/currency/usd/').text
    soup = BeautifulSoup(req, 'lxml')
    dollar = float(soup.find(class_='Text__sc-j452t5-0 bCCQWi').text.split()[0].replace(',', '.'))
    return dollar


def rewrite_json(data: dict, dollar: float) -> dict:
    """This funciton rewrite json and add some strings in json and return json-dict"""

    results = []
    for item in data:
        item_name = item['name']  # name of skin
        price = float(item['price'].replace('$', ''))  # price in dollars
        item_price = round(price * dollar, 2)  # price in RUB

        url = item['url']  # link for skin on lis-skins
        price_steam = item['price_steam']

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
    data = sorted(data, key=itemgetter('profit'), reverse=True)
    with open('final_result.json', 'w', encoding='utf-8') as file:  # Write result to json
        json.dump(data, file, indent=4, ensure_ascii=False)


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
            "price_steam": 821.37
        }
    ]
    dollar = get_dollar()
    results = rewrite_json(data, dollar)

    save_results(results)
