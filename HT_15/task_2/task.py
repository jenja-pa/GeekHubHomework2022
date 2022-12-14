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
import data_operations
import rozetka_api

if __name__ == "__main__":
    api = rozetka_api.Api()
    database = data_operations.DataBaseOperations()

    for item_id in data_operations.CsvOperations().load():
        print(f"From CSV {item_id=}")
        data = api.get_item_data(item_id)
        if data is None: 
            # Wrong ID - the message was derived by the method .get_item_data()
            continue
        database.insert(data)

    database.close()
