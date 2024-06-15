import json

from tools.drivers import SteamDriver
from tools.func import read_json, write_json, del_data_file
from tools.parsers import ParserSteam


def steam_parser(data: json, cant_find=False) -> json:
    """This func add in dict data one key (price_steam) and value (this value is prace in steam without commision)"""
    steam_driver = SteamDriver()
    steam_parser = ParserSteam()
    was_Exception = False

    results = []  # final results

    for count, item in enumerate(data):
        try:
            link = item['steam']
            steam_driver.url = link
            html = steam_driver.get_html()
            steam_parser.set_html(html)
            price = steam_parser.get_price()
            fast_price = steam_parser.get_fast_price()

            item["fast_price_steam"] = fast_price  # this key has value which include price in steam without commision
            item["price_steam"] = price  # this key has value which include price in steam without commision

            results.append(item)  # add information about item in list results

            print(f'[INFO] steam: {count + 1} / {len(data)}')  # info in console

        except Exception as ex:
            was_Exception = True  # if an exception occurred

            print(f'[WARNING] exception: {ex}')
            last_element_index = count + 1

            print(f'[INFO] {last_element_index} items were processed')
            print(f'[INFO] {len(data) - last_element_index} items were saved')

            # Saving remainining items in lis_skins.json
            remaining_items = data[last_element_index:]
            write_json('D:/Python_program/scraping_lis_skins/json/lis_skins.json', remaining_items)
            break

    if not was_Exception:  # if an exception occurred
        if cant_find:
            del_data_file('D:/Python_program/scraping_lis_skins/json/cant_find.json')
        else:
            del_data_file('D:/Python_program/scraping_lis_skins/json/lis_skins.json')

    write_json('D:/Python_program/scraping_lis_skins/json/steam.json', results)
    return results


if __name__ == '__main__':
    data = read_json('D:/Python_program/scraping_lis_skins/json/lis_skins.json')

    diction = steam_parser(data)
    print(diction)
