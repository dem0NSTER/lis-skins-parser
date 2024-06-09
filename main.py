import json

from func import rewrite_json, save_results, get_dollar
from lis_skins_parser import lis_skins_parser
from steam_parser import steam_parser

# collect data from lis_skins and save this in lis_skins.json
lis_skins_parser(
    'https://lis-skins.ru/market/csgo/?category_id=10%2C3%2C7%2C28%2C19%2C11%2C32&price_from=3&price_to=5&hold=-1&is_without_souvenir=1')

with open('lis_skins.json', encoding='utf-8') as file:
    lis_skins_data = json.load(file)

# add one key and value in diction (price in steam)
results = steam_parser(lis_skins_data)

# rewrite json: add line "profit"
dollar = get_dollar()
final_data = rewrite_json(results, dollar)

# save results in json file (final_result.json)
save_results(final_data)

print('[INFO] everythink was ok!')
input('press enter to exit')
