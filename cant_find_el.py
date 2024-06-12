from parsers.steam_parser import steam_parser
from tools.func import rewrite_json, save_results, get_dollar, del_data_file, read_json


cant_find_data = read_json('json/cant_find.json')

# add one key and value in diction (price in steam)
steam_parser(cant_find_data)

steam_data = read_json('json/steam.json')

# rewrite json: add line "profit" and add file
results = rewrite_json(steam_data)

# save results in json file (final_result.json)
save_results(results, 'a')

del_data_file('json/cant_find.json')
