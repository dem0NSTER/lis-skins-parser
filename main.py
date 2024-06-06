from drivers import SteamDriver

data = [{
    "name": "StatTrak™ USP-S | Black Lotus (Field-Tested)",
    "price": "3.06$",
    "discount": "-32%",
    "url": "https://lis-skins.ru/market/csgo/stattrak-usp-s-black-lotus-field-tested/?hold=-1",
    "steam": "https://steamcommunity.com/market/listings/730/StatTrak™ USP-S | Black Lotus (Field-Tested)"
},
    {
        "name": "Glock-18 | Nuclear Garden (Minimal Wear)",
        "price": "2.56$",
        "discount": "-31%",
        "url": "https://lis-skins.ru/market/csgo/glock-18-nuclear-garden-minimal-wear/?hold=-1",
        "steam": "https://steamcommunity.com/market/listings/730/Glock-18 | Nuclear Garden (Minimal Wear)"
    }]

driver = SteamDriver()
count = 1

for item in data:
    driver.url = item['steam']
    driver.get_html()

    with open(f'steam_{count}.html', 'w', encoding='utf-8') as file:
        file.write(driver.html)
    count += 1
