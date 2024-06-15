from parsers.steam_parser import steam_parser
from tools.func import rewrite_json, save_results, read_json


def not_processed_elements(fast_profit=False):
    lis_skins_data = read_json('json/lis_skins.json')

    # add one key and value in diction (price in steam)
    steam_parser(lis_skins_data)

    steam_data = read_json('json/steam.json')

    # rewrite json: add line "profit" and add file
    results = rewrite_json(steam_data)

    # save results in json file (final_result.json)
    save_results(results, 'a', fast_profit=fast_profit)


if __name__ == '__main__':
    not_processed_elements()
