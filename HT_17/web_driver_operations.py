# web_driver_operations.py
"""
Операції полегшення роботи з WebDriver
"""
import time

# from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class WebDriver:
    def __init__(self, url_start):
        self._driver = Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            # options=self.__options
            )
        # self._driver.set_window_size(600, 600)
        self._wait = WebDriverWait(self._driver, 10)
        self._driver.get(url_start)


    def __options(self):
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--ignore-ssl-errors=true")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")
        # options.add_argument("--window-size=1800,1600")
        # options.add_argument('window-size=1920x1080');
        options.add_argument("--start-maximized")

        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        options.add_experimental_option(
            'prefs', 
            {
                'profile.default_content_setting_values.notifications': 2,
                'profile.default_content_settings.popups': 0
            })

        return options

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._driver.quit()

    def implicitly_wait(self, value):
        self._driver.implicitly_wait(value)

    def goto_page_order(self):
        a_elements = self._driver.find_elements(By.LINK_TEXT, "Order your robot!")
        if not a_elements:
            raise Exception("Sorry not found anchor to transition on page order")
        elif len(a_elements) > 1:
            raise Exception("Sorry multiplie results of ancher")
        a_elements[0].click()

        dialog_element = self._wait.until(EC.presence_of_element_located((By.CLASS_NAME, "modal-body")))
        if not dialog_element:
            raise Exception("Sorry not found dialog element")
    
        dialog_buttons = self._driver.find_elements(By.CSS_SELECTOR, ".modal-body .alert-buttons .btn-dark")
        if not dialog_buttons:
            raise Exception("Sorry not found dialog button")
        elif len(dialog_buttons) > 1:
            raise Exception("Sorry multiplie results of ancher dialog button")
        dialog_buttons[0].click() 
           
    def set_head(self, value):
        head_elements = self._driver.find_elements(By.ID, "head")
        if not head_elements:
            raise Exception("Sorry not found element to set head type")
        elif len(head_elements) > 1:
            raise Exception("Sorry multiplie results head tupe element")
        select_head_element = Select(head_elements[0])
        select_head_element.select_by_value(f'{value}')

    def set_body(self, value):
        body_elements = self._driver.find_elements(By.CSS_SELECTOR, f".stacked input[name='body'][value='{value}']")
        if not body_elements:
            raise Exception("Sorry not found element to set body type")
        elif len(body_elements) > 1:
            raise Exception("Sorry multiplie results body tupe element")
        body_elements[0].click()
                
    def set_legs(self, value):
        legs_elements = self._driver.find_elements(By.XPATH, "//div[@class='form-group'][contains(label/text(), 'Legs')]/input")
        if not legs_elements:
            raise Exception("Sorry not found element to set legs")
        elif len(legs_elements) > 1:
            raise Exception("Sorry multiplie results legs element")
        legs_elements[0].clear()    
        legs_elements[0].send_keys(str(value))

    def set_address(self, value):
        address_element = self._find_element(By.ID, "address", "address element")
        address_element.clear()
        address_element.send_keys(str(value))
        # self._driver.execute_script('arguments[0].scrollIntoView({block: "center"});', address_element)

    def get_preview(self, temp_file_name="preview_robot"):
        # self._driver.execute_script("document.body.style.zoom='75%'")
        # time.sleep(1)

        btn_preview = self._find_element(By.ID, "preview", "preview robot button")
        btn_preview.click()

        img_element = self._wait.until(EC.presence_of_element_located((By.ID, "robot-preview-image")))
        if not img_element:
            raise Exception("Sorry not found img preview robot")

        # actions = ActionChains(self._driver)
        # actions.move_to_element(img_element).perform()

        # el = self._find_element(By.TAG_NAME, "html", "body element")
        # el.send_keys(Keys.CONTROL + Keys.SUBTRACT)
        # time.sleep(1)
        # el.send_keys(Keys.CONTROL + Keys.SUBTRACT)
        # time.sleep(1)
        img_element.screenshot(temp_file_name+".png")

        # el.send_keys(Keys.CONTROL, Keys.ADD)
        # time.sleep(1)
        # el.send_keys(Keys.CONTROL, Keys.ADD)

        # self._driver.execute_script("document.body.style.zoom='100%'")
        # time.sleep(2)

    def press_order(self):
        btn_order = self._find_element(By.ID, "order", "order robot button")
        order_bill_element = None

        print("Begin attempts to find bill order")
        for i in range(5):
            print(f"Attempt: {i}")
            btn_order.click()
            try:
                order_bill_element = self._wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//H3[contains(text(), 'Receipt')]")))
                if order_bill_element:
                    print(f"Bill order found {order_bill_element}")
                    break
            except TimeoutException:
                continue
                time.sleep(1)
        
        if order_bill_element is None:
            raise Exception("Error does not able order_bill_element after 5 attempts")

        print(f"{order_bill_element=}")
        order_number_element = self._find_element(By.XPATH, "//div[@id='receipt']/p[contains(@class, 'badge-success')]", "order number elenemt")
        print(f"{order_number_element=}")
        return order_number_element.text

    def _find_element(self, by, selector, description_element):
        elements = self._driver.find_elements(by, selector)
        if not elements:
            raise Exception(f"Sorry not found element {description_element}")
        elif len(elements) > 1:
            raise Exception(f"Sorry multiplie results for {description_element}")
        return elements[0]




"""

time.sleep(5)  # Let the user actually see something!

search_box = driver.find_element(by=By.NAME, value="q")

search_box.send_keys('ChromeDriver')

search_box.submit()

time.sleep(5)  # Let the user actually see something!
"""
