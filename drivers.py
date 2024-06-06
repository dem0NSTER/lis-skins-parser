import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException


class ChromeDriver:
    """Base class for drivers"""
    def __init__(self, url=''):
        self.url = url
        self.html = None
        self.driver = None
        self.__set_options()

    def __set_options(self) -> None:
        """This metod can set options for WebDriver (user agent and other important opitons)"""
        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument(
            'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
        self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option('useAutomationExtension', False)

    def create_driver(self) -> None:
        """This method make WedDriver. !!!Before you must use __set_options method!!!"""
        self.driver = webdriver.Chrome(options=self.__options)


class LisSkinsDriver(ChromeDriver):
    """Driver for lis-skins!!!"""
    def get_html(self) -> str:
        """this method get page's html code, return html code"""
        self.create_driver()

        self.driver.set_page_load_timeout(3)
        try:
            self.driver.get(self.url)
        except TimeoutException:
            self.driver.execute_script('window.stop()')

        self.html = self.driver.page_source
        self.driver.close()
        return self.html


class SteamDriver(ChromeDriver):
    def get_html(self) -> str:
        """this method get page's html code, return html code"""
        ...

    def apdate_cookies(self):
        ...


if __name__ == '__main__':
    driver = LisSkinsDriver(
        url=f'https://lis-skins.ru/market/csgo/awp/?price_from=1&price_to=5&is_without_souvenir=1&page={1}')

    # with open('index.html', 'w') as file:
    #     file.write(driver.get_html())
    page = 1

    while True:
        driver.url = f'https://lis-skins.ru/market/csgo/awp/?price_from=1&price_to=50&is_without_souvenir=1&page={page}'
        with open(f'index_{page}.html', 'w') as file:
            file.write(driver.get_html())

        last_page = 2
        if page == last_page:
            break
        page += 1
