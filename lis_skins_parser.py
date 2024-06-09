from drivers import LisSkinsDriver
from parsers import ParserLisSkins


def lis_skins_parser(url: str) -> None:
    """This funcion collect data from Lis-skins and then make json file with all data"""
    driver = LisSkinsDriver()
    parser = ParserLisSkins()
    page = 1

    while True:
        driver.url = f'{url}&page={page}'
        html = driver.get_html()
        parser.set_html(html)
        last_page = parser.get_count_pages()
        parser.get_data_on_page()

        print(f'[INFO] lis-skins: {page} / {last_page}')
        if page == last_page:
            break
        page += 1

    parser.write_file()


if __name__ == '__main__':
    lis_skins_parser('https://lis-skins.ru/market/csgo/?category_id=10%2C3%2C7%2C28%2C19%2C11%2C32&price_from=3&price_to=5&is_without_souvenir=1')
