import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver, query):
    driver.get("http://www.google.com")
    try:
        box = driver.wait.until(EC.presence_of_element_located(
            (By.NAME, "q")))
        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "btnK")))
        box.send_keys(query)
        button.click()
    except TimeoutException:
        print("Box or Button not found in google.com")


if __name__ == "__main__":
    driver = init_driver()
    lookup(driver, "Selenium")
    time.sleep(5)
    driver.quit()

# SELENIUM TRY

# div class js-more / a class btn btn-default btn-lg btn-outline u-text-h2 <<<<<---- click on this
#
# page = requests.get('https://tsn.ua/search?query=нато')
# tree = html.fromstring(page.content)
# title = tree.xpath('//div[@class="c-feed t-feed-list t-feed-list-lg js-more-block"]//div[@class="c-post-meta"]/h4/a/text()')
# print(title)
# driver.find_element_by_css_selector('.button.c_button.s_button').click()
