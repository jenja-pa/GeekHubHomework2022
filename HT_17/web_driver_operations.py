# web_driver_operations.py
"""
Операції полегшення роботи з WebDriver
"""
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement


class NotFoundElementError(Exception):
    pass


class MultieElementsError(Exception):
    pass


class MyWebDriver:
    def __init__(self, url_start):
        self._driver = Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=self.__options()
            )
        self.cnt_attempt = 10
        self._wait = WebDriverWait(self._driver, 1)
        self._driver.get(url_start)

    def __options(self):
        options = ChromeOptions()
        options.page_load_strategy = 'normal'
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
        options.add_argument("--window-size=1800,1600")
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

    def save_page_source(self, f_name):
        """
        Допоміжна функція контролю завантаженої сторінки
        """
        print("save page_source")
        with open(f_name, "w", encoding="utf-8") as f:
            f.write(self._driver.page_source)

    def goto_page_order(self):
        a_element = self._find_element(
            By.LINK_TEXT,
            "Order your robot!",
            "Link swith to order robot")
        a_element.click()

        # виявляємо та натискаємо на кнопку спливаючого вікна перед заказом
        form_element = self._order_popup_form_wait()
        if self._is_order_popup_form_visible(form_element):
            self._order_popup_form_close(form_element)

    def set_head(self, value):
        head_element = self._find_element(By.ID, "head", "input head element")
        select_head_element = Select(head_element)
        select_head_element.select_by_value(f'{value}')

    def set_body(self, value):
        body_element = self._find_element(
            By.CSS_SELECTOR,
            f".stacked input[name='body'][value='{value}']",
            "input type body element")
        body_element.click()

    def set_legs(self, value):
        legs_element = self._find_element(
            By.XPATH,
            "//div[@class='form-group'][contains(label/text(), 'Legs')]/input",
            "input count of legs element"
            )
        legs_element.clear()
        legs_element.send_keys(str(value))

    def set_address(self, value):
        address_element = self._find_element(
            By.ID,
            "address",
            "input address element")
        address_element.clear()
        address_element.send_keys(str(value))

    def get_preview(self, temp_file_name="preview_robot"):
        btn_preview = self._find_element(
            By.ID,
            "preview",
            "preview robot button")
        btn_preview.click()

        img_elements = self._wait.until(
            EC.presence_of_element_located((By.ID, "robot-preview-image")))
        if not img_elements:
            raise Exception("Sorry not found img preview robot")
        self._wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#robot-preview-image img[alt='Head']")
                ))
        self._wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#robot-preview-image img[alt='Body']"),
                ))
        self._wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#robot-preview-image img[alt='Legs']")
                ))

        img_elements.screenshot(temp_file_name+".png")

    def press_order(self):
        btn_order = self._find_element(By.ID, "order", "order robot button")

        order_bill_element = None
        print("Begin attempts to find bill order")
        flag_success_get_bill_element = False
        for i in range(self.cnt_attempt):
            print(f"Attempt: {i + 1}. ", end="")
            btn_order.click()
            try:
                order_bill_element = self._wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//H3[contains(text(), 'Receipt')]")
                    ))
                if order_bill_element:
                    # Bill order form does found
                    flag_success_get_bill_element = True
                    break
            except TimeoutException:
                print("Attempt wrong. Try again.")
        # End decor output message
        if flag_success_get_bill_element:
            print("Attempt success.")
        else:
            print()
            raise Exception(f"After {self.cnt_attempt} - does not success "
                            f"getting order bill element, process will be "
                            f"terminate")

        if order_bill_element is None:
            raise Exception(
                f"Error does not able order_bill_element after "
                f"{self.cnt_attempt} attempts")

        order_number_element = self._find_element(
            By.XPATH,
            "//div[@id='receipt']/p[contains(@class, 'badge-success')]",
            "order number elenemt")
        print(f"Bill order does found {order_number_element.text}")
        return order_number_element.text

    def click_to_goto_new_order(self):
        # Натискаємо на кнопку заказа наступного робота
        btn_new_order = self._find_element(
            By.ID,
            "order-another",
            "order another robot button")
        btn_new_order.click()
        # виявляємо та натискаємо на кнопку спливаючого вікна перед заказом
        form_element = self._order_popup_form_wait()
        if self._is_order_popup_form_visible(form_element):
            self._order_popup_form_close(form_element)

    def _find_element(self, by, selector, description_element):
        elements = self._driver.find_elements(by, selector)
        if not elements:
            raise NotFoundElementError(
                f"Sorry not found element {description_element}")
        elif len(elements) > 1:
            raise MultieElementsError(
                f"Sorry multiplie results for {description_element}")
        return elements[0]

    def _order_popup_form_wait(self):
        element = self._wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "modal-body")
            ))
        if element is None:
            raise NotFoundElementError(
                "Sorry element with CLASS_NAME modal-body not present")
        return element

    def _is_order_popup_form_visible(self, order_form_element):
        if isinstance(order_form_element, WebElement):
            return order_form_element.is_displayed()
        raise NotFoundElementError("Sorry element is not WebElement type")

    def _order_popup_form_close(self, order_form_element):
        dialog_buttons = order_form_element.find_elements(
            By.CSS_SELECTOR,
            ".modal-body .alert-buttons .btn-dark")
        if not dialog_buttons:
            raise NotFoundElementError("Sorry not found dialog button")
        elif len(dialog_buttons) > 1:
            raise MultieElementsError(
                "Sorry multiplie results of need dialog button")
        dialog_buttons[0].click()
