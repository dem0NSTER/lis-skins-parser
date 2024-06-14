import time
from Lib import pickle

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


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

    def headless(self):
        self.__options.add_argument('--headless')

    def create_driver(self) -> None:
        """This method make WedDriver. !!!Before you must use __set_options method!!!"""
        self.driver = webdriver.Chrome(options=self.__options)


class LisSkinsDriver(ChromeDriver):
    """Driver for lis-skins!!!"""

    def get_html(self) -> str:
        """this method get page's html code, return html code"""
        # self.headless()
        self.create_driver()

        self.driver.set_page_load_timeout(1.5)
        try:
            self.driver.get(self.url)
        except TimeoutException:
            self.driver.execute_script('window.stop()')

        try:
            self.__load_cookies()
        except TimeoutException:
            self.driver.execute_script('window.stop()')

        self.html = self.driver.page_source
        self.driver.close()
        return self.html

    def update_cookies(self) -> None:
        """this method get page's html code, return html code"""
        # self.headless()
        self.create_driver()

        self.driver.set_page_load_timeout(10)
        try:
            self.driver.get(
                'https://lis-skins.ru/market/csgo/awp-fever-dream-battle-scarred/?hold=-1')
        except TimeoutException:
            self.driver.execute_script('window.stop()')
        time.sleep(5)

        pickle.dump(self.driver.get_cookies(), open('D:/Python_program/scraping_lis_skins/cookie/cookies_lis_skins', 'wb'))
        time.sleep(1)
        self.driver.close()

    def __load_cookies(self) -> None:
        """This mehtod used for load your cookies"""
        for cookie in pickle.load(open('D:/Python_program/scraping_lis_skins/cookie/cookies_lis_skins', 'rb')):
            self.driver.add_cookie(cookie)
        time.sleep(0.1)
        self.driver.refresh()


class SteamDriver(ChromeDriver):
    def get_html(self) -> str:
        """this method get page's html code, return html code"""
        self.headless()
        self.create_driver()
        self.driver.get(self.url)
        self.__load_cookie()
        self.html = self.driver.page_source
        self.driver.close()
        return self.html

    def update_cookies(self):
        """This method can updata your cookies"""
        self.create_driver()
        self.driver.get('https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20%28Field-Tested%29')
        time.sleep(4)
        self.driver.find_element(By.CLASS_NAME, 'global_action_link').click()
        time.sleep(30)

        pickle.dump(self.driver.get_cookies(), open('D:/Python_program/scraping_lis_skins/cookie/cookies', 'wb'))
        time.sleep(1)

        self.driver.close()

    def __load_cookie(self):
        """This mehtod used for load your cookies"""
        for cookie in pickle.load(open('D:/Python_program/scraping_lis_skins/cookie/cookies', 'rb')):
            self.driver.add_cookie(cookie)
        time.sleep(0.1)
        self.driver.refresh()
        time.sleep(0.3)


if __name__ == '__main__':
    driver = SteamDriver()
    driver.url = 'https://steamcommunity.com/market/listings/730/Operation%20Riptide%20Case'
    html = driver.get_html()
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(html)
