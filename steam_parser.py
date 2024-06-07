import json

from drivers import SteamDriver
from parsers import ParserSteam


def steam_parser(data: dict) -> dict:
    """This func add in dict data one key (price_steam) and value (this value is prace in steam without commision"""
    steam_driver = SteamDriver()
    steam_parser = ParserSteam()

    for item in data:
        link = item['steam']
        steam_driver.url = link
        html = steam_driver.get_html()
        steam_parser.set_html(html)
        price = steam_parser.get_price()
        item["price_steam"] = price  # this key has value which include price in steam without commision

    return data


if __name__ == '__main__':
    data = [
        {
            "name": "Desert Eagle | Crimson Web (Well-Worn)",
            "price": "6.61$",
            "discount": "-34%",
            "url": "https://lis-skins.ru/market/csgo/desert-eagle-crimson-web-well-worn/",
            "steam": "https://steamcommunity.com/market/listings/730/Desert Eagle | Crimson Web (Well-Worn)"
        },
        {
            "name": "StatTrak™ AK-47 | Slate (Battle-Scarred)",
            "price": "6.57$",
            "discount": "-34%",
            "url": "https://lis-skins.ru/market/csgo/stattrak-ak-47-slate-battle-scarred/",
            "steam": "https://steamcommunity.com/market/listings/730/StatTrak™ AK-47 | Slate (Battle-Scarred)"
        }
    ]

    diction = steam_parser(data)
    with open('final_result.json', 'w', encoding='utf-8') as file:
        json.dump(diction, file, ensure_ascii=False, indent=4)
