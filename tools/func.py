import json
from _operator import itemgetter
from json import JSONDecodeError


def is_empty_json(path: str) -> bool:
    """return True if json file has not any data"""
    try:
        data = read_json(path)
        if len(data) == 0:
            return True
        return False

    except JSONDecodeError:
        return True


def calculate_profit(price_steam: float, price_website: float) -> float:
    """This func can calculate profit, which you can get"""
    profit = (price_steam - price_website) / price_website
    final_profit = round(profit, 4) * 100
    return final_profit

def read_json(path: str) -> json:
    with open(path, encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_json(path: str, data, mode='w') -> None:
    """This function can write data to json file"""
    is_empty = is_empty_json(path)

    if mode == 'a' and not is_empty:  # append mode
        old_data = read_json(path)
        new_data = data
        data = old_data + new_data

    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


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
        price = item['price']  # price on lis-skins

        url = item['url']  # link for skin on lis-skins
        price_steam = item['price_steam']
        fast_price_steam = item['fast_price_steam']

        if price_steam == 0:  # if i cant find price in steam
            del item['price_steam']
            del item['fast_price_steam']
            cant_find_items.append(item)
            continue

        profit = calculate_profit(price_steam, price)
        fast_profit = calculate_profit(fast_price_steam, price)

        if profit < min_profit_you_want:
            continue

        results.append(
            {
                "name": item_name,
                "price": price,
                "price_steam": price_steam,
                "profit": profit,
                "fast_profit": fast_profit,
                "url": url
            }
        )
    print(f'[INFO] I can not find {len(cant_find_items)} elements')
    write_json('D:/Python_program/scraping_lis_skins/json/cant_find.json', cant_find_items, 'a')
    return results


def delete_dublicates_from_json(path: str) -> None:
    """This function can delete all recurring elements"""

    if is_empty_json(path):
        return

    items = read_json(path)

    data = set()
    unique_items = []

    for item in items:
        unique_key = (item['name'], item['price'], item['discount'], item['url'], item['steam'])
        if unique_key not in data:
            data.add(unique_key)
            unique_items.append(item)

    write_json(path, unique_items)
    print(f"Removed duplicates. {len(unique_items)} unique items saved.")


def save_results(data: json, mode='w', fast_profit=False) -> None:
    """This funciton sorted data and save all in final_results.json"""

    if mode == 'a':
        old_data = read_json('D:/Python_program/scraping_lis_skins/json/final_result.json')
        new_data = data
        data = old_data + new_data

    if fast_profit:
        data = sorted(data, key=itemgetter('fast_profit'), reverse=True)
    else:
        data = sorted(data, key=itemgetter('profit'), reverse=True)

    write_json('D:/Python_program/scraping_lis_skins/json/final_result.json', data)


def del_all_data():
    """del old data from files"""
    del_data_file('json/lis_skins.json')
    del_data_file('json/steam.json')
    del_data_file('json/cant_find.json')
    del_data_file('json/final_result.json')


if __name__ == '__main__':
    data = read_json('D:/Python_program/scraping_lis_skins/json/steam.json')
    data = rewrite_json(data)
    save_results(data, fast_profit=True)
