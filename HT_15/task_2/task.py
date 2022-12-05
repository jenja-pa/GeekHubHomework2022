# task.py
# Написати програму, яка має складатися з трьох файлів/модулів.
# - rozetka_api.py, де створти клас RozetkaAPI, який буде містити 
# метод get_item_data, який на вхід отримує id товара з сайту розетки 
# та повертає словник з такими даними: 
#   * item_id (він же і приймається на вхід), 
#   * title, 
#   * old_price, 
#   * current_price, 
#   * href (лінка на цей товар на сайті), 
#   * brand, 
#   * category. 
# Всі інші методи, що потрібні для роботи мають бути приватні/захищені.
# - data_operations.py з класами CsvOperations та DataBaseOperations. 
#   * CsvOperations містить метод для читання даних. 
# Метод для читання приймає аргументом шлях до csv файлу де в колонкі ID 
# записані як валідні, так і не валідні id товарів з сайту. 
#   * DataBaseOperations містить метод для запису даних в sqlite3 базу 
# і відповідно приймає дані для запису. 
# Всі інші методи, що потрібні для роботи мають бути приватні/захищені.
# - task.py - головний модуль, який ініціалізує і запускає весь процес.
# 
# Суть процесу: 
#  * читаємо ID товарів з csv файлу, 
#  * отримуємо необхідні дані і записуємо їх в базу. 
#  * Якщо ID не валідний/немає даних - вивести відповідне повідомлення 
#  * і перейти до наступного.

# Дані по товару без назви код 27714809
# https://common-api.rozetka.com.ua/v2/goods/get-price/?ids=27714809
# https://common-api.rozetka.com.ua/v2/goods/get-price/?country=UA&lang=ru&ids=27714809&with_show_in_site=1&lng=ru
# Дані про товар - повна
# https://rozetka.com.ua/api/product-api/v4/goods/get-main?front-type=xl&country=UA&lang=ru&goodsId=27714809
# https://rozetka.com.ua/api/product-api/v4/goods/get-main?country=UA&lang=ua&goodsId=27714809

import csv
from rozetka_api import Api as RozetkaApi # , Data as RozetkaData


if __name__ == "__main__":
    api = RozetkaApi()

    data = api.get_item_data(27714809)

    print(f"task: {data=}")

