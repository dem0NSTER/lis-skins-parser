from parsers.steam_parser import steam_parser
from tools.func import rewrite_json, save_results, get_dollar, read_json


lis_skins_data = read_json('json/lis_skins.json')

# add one key and value in diction (price in steam)
steam_parser(lis_skins_data)

steam_data = read_json('json/steam.json')

# rewrite json: add line "profit" and add file
dollar = get_dollar()
results = rewrite_json(steam_data, dollar)

# save results in json file (final_result.json)
save_results(results, mode='a')
