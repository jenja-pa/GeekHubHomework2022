# web_driver_operations.py
"""
Операції полегшення роботи з WebDriver
"""
from selenium import webdriver
from selenium.webdriver.common.by import By


class WebDriver:
    def __init__(self):
        self._driver = None

    def __enter__(self, url_start):
        self._driver = webdriver.Chrome()
        self._driver.get('http://www.google.com/')

    def __exit__(self):
        self._driver.quit()
        self._driver = None

    def find_element(by, search)







time.sleep(5)  # Let the user actually see something!

search_box = driver.find_element(by=By.NAME, value="q")

search_box.send_keys('ChromeDriver')

search_box.submit()

time.sleep(5)  # Let the user actually see something!

