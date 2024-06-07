from parsers import ParserSteam
from drivers import SteamDriver

data = [
    {
        "name": "StatTrak™ AK-47 | Phantom Disruptor (Battle-Scarred)",
        "price": "6.89$",
        "discount": "-35%",
        "url": "https://lis-skins.ru/market/csgo/stattrak-ak-47-phantom-disruptor-battle-scarred/",
        "steam": "https://steamcommunity.com/market/listings/730/StatTrak™ AK-47 | Phantom Disruptor (Battle-Scarred)"
    },
    {
        "name": "Souvenir AWP | Black Nile (Battle-Scarred)",
        "price": "6.83$",
        "discount": "-38%",
        "url": "https://lis-skins.ru/market/csgo/souvenir-awp-black-nile-battle-scarred/",
        "steam": "https://steamcommunity.com/market/listings/730/Souvenir AWP | Black Nile (Battle-Scarred)"
    }
]

steam_driver = SteamDriver()
steam_parser = ParserSteam()
# steam_driver.update_cookies()

for item in data:
    link = item['steam']
    steam_driver.url = link
    html = steam_driver.get_html()
    steam_parser.set_html(html)
    price = steam_parser.get_price()
    item["price_steam"] = price

print(data)
