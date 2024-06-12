import json
from _operator import itemgetter

from bs4 import BeautifulSoup
from tools.func import write_json


class ParserLisSkins:
    def __init__(self, html=''):
        self.html = html
        self.pages = 1
        self.__items_data = []
        self.soup = BeautifulSoup(self.html, 'lxml')

    def set_html(self, html: str) -> None:
        """This method can change html code which it scraping"""
        self.html = html
        self.soup = BeautifulSoup(self.html, 'lxml')

    def get_data_on_page(self) -> None:
        for item in self.__get_items():
            if not self.__check_discount(item):
                continue
            item_name = item.find_all('img')[-1].get('alt')
            item_price = item.find(class_='price').text.strip()
            item_price = float(item_price.replace(' ', ''))
            steam_url = 'https://steamcommunity.com/market/listings/730/' + item_name.replace('�', '™')
            item_url = item.find(class_='name').get('href')
            self.__add_item(
                {
                    'name': item_name,
                    'price': item_price,
                    'discount': self.__check_discount(item),
                    'url': item_url,
                    'steam': steam_url
                }
            )

    def get_count_pages(self) -> int:
        """Get count of pages"""
        data = self.soup.find_all(class_='page-link')
        if len(data) == 0:  # if websity have only on page!
            self.pages = 1
            return self.pages

        self.pages = int(data[-2].text)
        return self.pages

    def write_file(self) -> None:
        """This method write data about items to json file (results.json)"""
        data = sorted(self.__items_data, key=itemgetter('discount'), reverse=True)
        write_json('D:/Python_program/scraping_lis_skins/json/lis_skins.json', data)

    def __get_items(self) -> list:
        """Get all items on this page"""
        return self.soup.find_all(lambda tag: tag.get('data-id') is not None)

    def __add_item(self, data: dict) -> None:
        """This method add data of item in dict with data about all items"""
        self.__items_data.append(data)

    @staticmethod
    def __check_discount(item: BeautifulSoup) -> bool or int:
        """This method check discount on item and return Fasle, if item has not discount or discount too low, or return discount"""
        item_discount = item.find(class_='steam-price-discount')
        if item_discount and int(item_discount.text.strip().replace('%', '')) < -30:
            return item_discount.text.strip()
        return False


class ParserSteam:
    def __init__(self, html=''):
        self.html = html
        self.soup = BeautifulSoup(self.html, 'lxml')
        self.steam_price = None

    def set_html(self, html: str) -> None:
        """This method can change html code which it scraping"""
        self.html = html
        self.soup = BeautifulSoup(self.html, 'lxml')

    def get_price(self) -> float:
        """This method can get steam price of this skin and return it"""
        price_list = self.soup.find_all(class_='market_listing_price market_listing_price_without_fee')

        if len(price_list) == 0:
            self.steam_price = 0
            return self.steam_price

        for price in price_list:
            if price.text.strip() == 'Продано!':
                continue
            skin_price = price.text.strip().split()

            if skin_price[-1] != 'pуб.':
                raise ValueError('cookies error')

            self.steam_price = float(skin_price[0].replace(',', '.'))
            break
        return self.steam_price


if __name__ == '__main__':
    parser = ParserLisSkins()
    page = 1

    while True:
        with open(f'index_{page}.html') as file:
            src = file.read()

        parser.set_html(src)
        count = parser.get_count_pages()
        parser.get_data_on_page()

        last_page = 2
        if page == last_page:
            break
        page += 1

    print(count)
    parser.write_file()
