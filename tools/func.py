import json
from _operator import itemgetter

import requests
from bs4 import BeautifulSoup


def read_json(path: str) -> json:
    with open(path, encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_json(path: str, data, mode='w') -> None:
    with open(path, mode, encoding='utf-8') as file:
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


def rewrite_json(data: json, min_profit_you_want=25) -> json:
    """This funciton rewrite json and add some strings in json and return list which include two json files:"""

    cant_find_items = []  # for item where I can find price in steam
    results = []

    for item in data:
        item_name = item['name']  # name of skin
        price = item['price']  # price in dollars

        url = item['url']  # link for skin on lis-skins
        price_steam = item['price_steam']
        if price_steam == 0:  # if i cant find price in steam
            del item['price_steam']
            cant_find_items.append(item)
            write_json('D:/Python_program/scraping_lis_skins/json/cant_find.json', cant_find_items)
            continue

        profit = (price_steam - price) / price
        final_profit = round(profit, 4) * 100

        if final_profit < min_profit_you_want:
            continue

        results.append(
            {
                "name": item_name,
                "price": price,
                "price_steam": price_steam,
                "profit": final_profit,
                "url": url
            }
        )
    print(f'[INFO] I can not find {len(cant_find_items)} elements')
    return results


def save_results(data: json, mode='w') -> None:
    """This funciton sorted data and save all in final_results.json"""

    if mode == 'a':
        old_data = read_json('D:/Python_program/scraping_lis_skins/json/final_result.json')
        new_data = data
        data = old_data + new_data

    data = sorted(data, key=itemgetter('profit'), reverse=True)
    write_json('D:/Python_program/scraping_lis_skins/json/final_result.json', data)


def del_all_data():
    # del old data from files
    del_data_file('json/lis_skins.json')
    del_data_file('json/steam.json')
    del_data_file('json/cant_find.json')
    del_data_file('json/final_result.json')


if __name__ == '__main__':
    data = read_json('D:/Python_program/scraping_lis_skins/json/steam.json')

    results = rewrite_json(data)

    save_results(results)
