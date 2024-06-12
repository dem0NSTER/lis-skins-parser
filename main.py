from parsers.lis_skins_parser import lis_skins_parser
from parsers.steam_parser import steam_parser
from tools.func import rewrite_json, save_results, del_all_data, read_json

del_all_data()  # delete data from files

base_url = 'https://lis-skins.ru/market/csgo/?category_id=19%2C11%2C32%2C3%2C7%2C28%2C10&price_from=1&price_to=2&hold=-1&is_without_souvenir=1'
lis_skins_parser(base_url)  # collect data from lis_skins and save this in lis_skins.json

lis_skins_data = read_json('json/lis_skins.json')

# add one key and value in diction (price in steam)
steam_parser(lis_skins_data)

steam_data = read_json('json/steam.json')

# rewrite json: add line "profit" and add file
results = rewrite_json(steam_data)

# save results in json file (final_result.json)
save_results(results)
