import json

from bs4 import BeautifulSoup


class ParserLisSkins:
    def __init__(self, html: str, base_url: str):
        self.data = html
        self.base_url = base_url
        self.pages = 1
        self.__items_data = []
        self.soup = BeautifulSoup(self.data, 'lxml')

    def get_count_pages(self) -> int:
        """Get count of pages"""
        self.pages = int(self.soup.find_all(class_='page-link')[-2].text)
        return self.pages

    def get_data_on_page(self) -> None:
        for item in self.__get_items():
            if not self.__check_discount(item):
                continue
            item_name = item.find(class_='name-inner').text.strip()
            item_price = item.find(class_='price').text.strip()
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
        self.__write_file()

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

    def __write_file(self) -> None:
        """This method write data about items to json file (results.json)"""
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(self.__items_data, f, ensure_ascii=False, indent=4)
