import time
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(3)
try:
    driver.get("https://lis-skins.ru/market/csgo/?price_from=70&price_to=1000&is_without_souvenir=1")

except TimeoutException:
    driver.execute_script('window.stop()')

html = driver.page_source

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(html)


# driver.get("https://lis-skins.ru/market/csgo/?price_from=70&price_to=1000&is_without_souvenir=1")
# time.sleep(100000)
# page = driver.page_source
#
# driver.close()
# print(page)
