import time

from tools.func import is_empty_json
from not_processed_el import not_processed_elements
from cant_find_el import cant_find_elements
from first_el import first_elements


def main(lis_skins_base_url, fast_profit=False):
    first = True
    while True:
        if first:
            print('[INFO] start furst time')
            first_elements(base_url=lis_skins_base_url, fast_profit=fast_profit)
            first = False
            time.sleep(4)
            print('[INFO] first time ended')

        if not is_empty_json('D:/Python_program/scraping_lis_skins/json/lis_skins.json'):
            print('[INFO] start not processed elements')
            not_processed_elements(fast_profit=fast_profit)
            print('[INFO] end not processed elements')
            time.sleep(3)
            continue

        print('[INFO] lis_skins.json is empty. The only thing left to do is to process the items not found')

        if not is_empty_json('D:/Python_program/scraping_lis_skins/json/cant_find.json'):
            cant_find_elements(fast_profit=fast_profit)

        if is_empty_json('D:/Python_program/scraping_lis_skins/json/lis_skins.json') and is_empty_json('D:/Python_program/scraping_lis_skins/json/cant_find.json'):
            print('[INFO] everythig is ok')
            break


if __name__ == '__main__':
    url = 'https://lis-skins.ru/market/csgo/?category_id=19%2C11%2C32%2C3%2C7%2C28%2C10&price_from=350&price_to=1000&hold=-1&is_without_souvenir=1'
    fast_url = 'https://lis-skins.ru/market/csgo/?type_id=46%2C48%2C49%2C47%2C50%2C51&price_from=50&price_to=70&hold=-1'
    main(lis_skins_base_url=fast_url, fast_profit=True)
