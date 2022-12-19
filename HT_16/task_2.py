# task_2.py
"""
Викорисовуючи Scrapy, написати скрипт,
який буде приймати на вхід:
 * назву та ID категорії (у форматі назва/id/)
із сайту https://rozetka.com.ua
і буде збирати всі товари із цієї
категорії, збирати по ним всі можливі дані:
 * бренд,
 * категорія,
 * модель,
 * ціна,
 * рейтинг
 * тощо)
і зберігати їх у CSV файл
> (наприклад, якщо передана категорія:
 * mobile-phones/c80003/,
то файл буде називатися c80003_products.csv)

П.С. Запуск кожного процесу відбувається
шляхом запуску відповідного файлу task.py
(як до цього запускалися попередні
домашки), а не через консоль.
(гугл підкаже how to start scrapy programmatically)

П.С.С У завданні 2 назву категорії просто
 збережіть у змінну (не треба робити
 через input())
"""

from scrapy_crawlers.run_spider_rozetka_category import run_spider

sample_categories_list = [
    "mobile-phones/c80003",
    "mugskie-vetnamki-shlepantsi-sabo/c4634817/",
    "sokovarki/c4626796/",
]

# input_parameter = "mobile-phones/c80003"
input_parameter = sample_categories_list[1]


if __name__ == "__main__":
    run_spider("scrapy_crawlers", input_parameter)
