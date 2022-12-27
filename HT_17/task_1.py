"""
Автоматизувати процес замовлення робота за допомогою Selenium

1. Отримайте та прочитайте дані з
 https://robotsparebinindustries.com/orders.csv
Увага! Файл має бути прочитаний з сервера кожного разу при
 запуску скрипта, не зберігайте файл локально.

2. Зайдіть на сайт https://robotsparebinindustries.com/

3. Перейдіть у вкладку "Order your robot"

4. Для кожного замовлення з файлу реалізуйте наступне:
    - закрийте pop-up, якщо він з'явився.
        Підказка: не кожна кнопка його закриває.
    - оберіть/заповніть відповідні поля для замовлення
    - натисніть кнопку Preview та збережіть зображення
        отриманого робота.
        Увага! Зберігати треба тільки зображення робота,
        а не всієї сторінки сайту.
    - натисніть кнопку Order та збережіть номер чеку.
        Увага! Інколи сервер тупить і видає помилку, але повторне
        натискання кнопки частіше всього вирішує проблему.
        Дослідіть цей кейс.
    - переіменуйте отримане зображення у формат:
        <номер чеку>_robot.
        Покладіть зображення в директорію output
        (яка має створюватися/очищатися під час запуску скрипта).
    - замовте наступного робота (шляхом натискання відповідної
    кнопки)

5. Для загального розуміння можна переглянути відео
https://www.youtube.com/watch?v=0uvexJyJwxA&ab_channel=Robocorp

** Додаткове завдання (необов'язково)
    - окрім збереження номеру чеку збережіть також
        HTML-код всього чеку
    - збережіть отриманий код в PDF файл
    - додайте до цього файлу отримане зображення робота
    (бажано на одній сторінці, але не принципово)
    - збережіть отриманий PDF файл у форматі <номер чеку>_robot
     в директорію output.
     Окремо зображення робота зберігати не потрібно. (edited)

Основне завдання виконано.
В Понеділок, Вівторок - спробую реалізувати:
  * лог виконання операцій заказу;
  * формування PDF чека заказа - файла на основі генерованого HTML;
    """
import os

from csv_operations import CsvUrlReader
from web_driver_operations import MyWebDriver


class Placer:
    def __init__(self, driver: MyWebDriver):
        self._driver = driver
        # goto page order from start
        self._driver.goto_page_order()

    def set_order(self, order):
        self._driver.set_head(order["Head"])
        self._driver.set_body(order["Body"])
        self._driver.set_legs(order["Legs"])
        self._driver.set_address(order["Address"])

        self._driver.get_preview("preview_robot")

        receipt_number = self._driver.press_order()
        os.rename(
            "preview_robot.png", 
            f"output/{receipt_number}_robot.png")

        self._driver.click_to_goto_new_order()


def empty_output_dir():
    if not os.path.exists("output"):
        os.makedirs('output')
    files = os.listdir("output")
    for file in files:
        os.remove(os.path.join('output/', file))


def main():
    try:
        url_orders = 'https://robotsparebinindustries.com/orders.csv'
        # todo - return empty_dir back
        empty_output_dir()
        with MyWebDriver('https://robotsparebinindustries.com/') as driver:
            placer = Placer(driver)
            for idx, order in enumerate(CsvUrlReader(url_orders)):
                print(f"{idx + 1}.{order=}")
                placer.set_order(order)
    except Exception:
        raise


if __name__ == "__main__":
    main()
