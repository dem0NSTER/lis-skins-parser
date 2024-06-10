import json

from tools.func import rewrite_json, save_results, get_dollar, del_data_file, read_json
from parsers.lis_skins_parser import lis_skins_parser
from parsers.steam_parser import steam_parser

# del old data from files
del_data_file('json/lis_skins.json')
del_data_file('json/steam.json')
del_data_file('json/cant_find.json')
del_data_file('json/final_result.json')

# collect data from lis_skins and save this in lis_skins.json
lis_skins_parser(
    'https://lis-skins.ru/market/csgo/?category_id=19%2C11%2C32%2C3%2C7%2C28%2C10&price_from=3&price_to=4&hold=-1&is_without_souvenir=1')

lis_skins_data = read_json('json/lis_skins.json')

# add one key and value in diction (price in steam)
steam_parser(lis_skins_data)


steam_data = read_json('json/steam.json')

# rewrite json: add line "profit" and add file
dollar = get_dollar()
results = rewrite_json(steam_data, dollar)

# save results in json file (final_result.json)
save_results(results)
