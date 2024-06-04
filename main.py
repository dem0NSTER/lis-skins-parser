import time

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.get("https://lis-skins.ru/market/csgo/?price_from=70&price_to=1000&is_without_souvenir=1")
time.sleep(1)
page = driver.page_source

driver.close()
print(page)
