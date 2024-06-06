from drivers import LisSkinsDriver
from parsers import ParserLisSkins

driver = LisSkinsDriver()
parser = ParserLisSkins()
page = 1

while True:
    driver.url = f'https://lis-skins.ru/market/csgo/?category_id=3%2C10%2C139%2C19%2C11%2C32&price_from=1&price_to=5&hold=-1&is_without_souvenir=1page={page}'
    html = driver.get_html()
    parser.set_html(html)
    last_page = parser.get_count_pages()
    parser.get_data_on_page()

    print(f'{page} / {last_page}')
    if page == last_page:
        break
    page += 1

parser.write_file()
