# test_webdriver.py
import time

# from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException


options = ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-web-security")
options.add_argument("--allow-running-insecure-content")
options.add_argument("--hide-scrollbars")
options.add_argument("--disable-setuid-sandbox")
options.add_argument("--profile-directory=Default")
options.add_argument("--ignore-ssl-errors=true")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("")
options.add_argument("--disable-gpu")
# options.add_argument("--window-size=800,600")

options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('prefs', {
                'profile.default_content_setting_values.notifications': 2,
                'profile.default_content_settings.popups': 0
            })

# driver = webdriver.Chrome()
# driver = webdriver.Chrome(ChromeDriverManager().install())
print(ChromeService(ChromeDriverManager().install()))
driver = Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options)

driver.get('http://www.google.com/')

time.sleep(2)  # Let the user actually see something!

search_box = driver.find_element(by=By.NAME, value="q")

search_box.send_keys('ChromeDriver')

search_box.submit()

time.sleep(2)  # Let the user actually see something!

driver.quit()


"""

експериментальні опції
'excludeSwitches', ['enable-automation']
'prefs', {
                'profile.default_content_setting_values.notifications': 2,
                'profile.default_content_settings.popups': 0
            }
"""
