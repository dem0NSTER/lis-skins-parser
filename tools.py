import time

from bs4 import BeautifulSoup
from selenium import webdriver


class ChromeDriver:
    """Driver for lis-skins!!!"""

    def __init__(self, url: str):
        self.url = url
        self.html = None
        self.__set_options()

    def __set_options(self) -> None:
        """This metod can set options for WebDriver (user agent and other important opitons)"""
        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
        self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option('useAutomationExtension', False)

    def __create_driver(self) -> None:
        """This method make WedDriver. !!!Before you must use __set_options method!!!"""
        self.__driver = webdriver.Chrome(options=self.__options)

    def get_html(self) -> str:
        """this method get page's html code, return html code"""
        self.__create_driver()
        self.__driver.get(self.url)
        time.sleep(1)
        self.html = self.__driver.page_source
        self.__driver.close()
        self.__driver.quit()
        return self.html

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        if not type(url) == str:
            raise ValueError('invalid link')

        if not 'lis-skins.ru' in url:
            raise ValueError('invalid link')

        self.__url = url


class ParserLisSkins:
    def __init__(self, html: str, base_url: str):
        self.data = html
        self.base_url = base_url
        self.pages = 1
        self.__items_data = []
        self.soup = BeautifulSoup(self.data, 'lxml')

    def get_pages(self) -> int:
        """Get count of pages"""
        self.pages = int(self.soup.find_all(class_='page-link')[-2].text)
        return self.pages

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

    def get_data_on_page(self):
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
        return self.__items_data


if __name__ == '__main__':
    # driver = ChromeDriver("https://lis-skins.ru/market/csgo/?price_from=1&price_to=7&is_without_souvenir=1")
    # print(driver.html)
    # driver.get_html()
    # with open('index.html', 'w') as file:
    #     file.write(driver.html)

    with open('index.html') as file:
        src = file.read()

    parser = ParserLisSkins(src, 'https://lis-skins.ru/market/csgo/?price_from=1&price_to=7&is_without_souvenir=1')
    print(parser.get_data_on_page())
