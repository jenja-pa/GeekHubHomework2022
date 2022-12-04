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

import requests
import csv

session = requests.Session()

headers = {
    "authority": "rozetka.com.ua",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=utf-8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
# cookie: ab-catalog-filters-index=off; delivery=new; uss_evoid_cascade=yes; ab-catalog-backend=old; cart-modal=cart-page; fit-size=new; ab-auto-portal=old; filter-tabs=old; ab-catalog-delivery-terms=old; ab-catalog-selection-filters=old; promo-horizontal-filters=verticalFilters; ab-catalog-tile-description=old; ab-catalog-filter-result-quantity=old; ab-kt-action=super-offer; fingerprint=off; skip-add-phone=off; social-auth=old; xab_segment=102; xl_uid=Cgo8CWOM7K2acDS5ij7gAg==; ab_language=new; slang=ru; uid=Cgo9D2OM7K22FSdR9UezAg==; visitor_city=24098; _uss-csrf=46pHK+XnREv08gDsLyL0EZpyo8jr6DDyl2tcnqNikcUj2GXi; ussat_exp=1670223231; ussajwt=eyJhbGciOiJSUzI1NiIsImtpZCI6InVzc2F0LnYwIiwidHlwIjoiSldUIn0.eyJkZXRhaWxzIjoiZmViOGUzMWYyZWQzZDg5Yjc0MmJlZTlmZGFiZDNlODk1NjM2NGFmOTgxNWEzMDI0MmU4NGY4YmExYjY5ZTAwNzk0ODFlMzMzMzg2ODAyOTFlYTUwMjMxNmEzMTZiMjI0OWEyYzFiNjk4MWM3OTdlYzQ2NDY1YTRhZmUwNjhjZGNkYjNlMmZlZWU2YTk1ZjVmYmNjMTVlYmU2OWIwODYyOTk5M2RlMWZmMjA2NDU2N2JhZmM2ODZkMjdiNjFkMmZjOTZjMzkwOTJmNmY0N2UyOThkZmY1NjdkNDgzMmRiZDQ0NWFmOWNjZjg2YWFlOTcxNDdhMDFmNjM0Nzg4ODk0YSIsImV4cCI6IjE2NzAyMjMyMzEiLCJ1c3NhdCI6IjVlZTMzMDk1ZTQ0NmNjYjgyMzM4MzE4NzA0NmU4YjA2LnVhLTZkM2FkMmM0NzlkYTQ1MDBkOWMzMjM1YTUyNjVhYjlkLjE2NzAyMjMyMzEifQ.hysKHyKZOoyyfRrEy-SUTVZgg-LiZDT9pjii5LR4OCFPtcwW3zfvVH0JtUf-yebvWmaFgIhmDURSAbXXjnWyaLlwTftCsojVNUctNb86JJnO47EDz1-D0nLI87_-Z1y_xMqKGnk-t2Lp9AMIpzKab-4udhQCs1y_Vaw5f6QqY9UOqaFZ-U1L7gBJjQHo0MkIhTc8qxIGjPEfvWBGyBfnyfh4gmbVhYyadZ0FsEybQhtkaEuRYKXf_iGB0Upsm2699R0ovOHNdZp1K9ekvid3mIQdkS1hCzmMxXc9bf4LTLAMMyAS9PX5jA_eFz_1iX-OND_7lkbLzsSQQWNX_MsnoA; ussat=5ee33095e446ccb823383187046e8b06.ua-6d3ad2c479da4500d9c3235a5265ab9d.1670223231; ussrt=b60d12ebaddc7456d93d9b18ed0dfbb1.ua-6d3ad2c479da4500d9c3235a5265ab9d.1672772031; ussapp=GFk4Qf_B-QhqDLzfilBGlxvyJlpJc0hDXXUZtsBp; _gcl_au=1.1.1046015480.1670180030; __utmz_gtm=utmcsr=google|utmccn=(none)|utmcmd=organic; _ga=GA1.3.26872181.1670180031; _gid=GA1.3.644252697.1670180031; afclid=13176071961670180035; _fbp=fb.2.1670180042366.1634198300; __exponea_etc__=9185546d-b426-404d-bb16-5e694365facc; __exponea_time2__=2.4725348949432373; __cf_bm=BDp_3HOzi5Io0sWh4SYept.7MHZNCCYaK9dBLsK3OYE-1670182838-0-ARMkfzjAAn4lUUTeiLv6iiQQcj6Nnk8XZWejD2iG4JJ0rJkLdcGQ2lS83FEF+y83TcO18Q57aArkek1Uv7jxfOs=

url = "https://rozetka.com.ua/api/product-api/v4/goods/get-main"
params = {"country": "UA", "lang": "ua", "goodsId": "27714809"}

response = session.get(url, headers=headers, params=params)

data = response.json()

print(f"{data=}")

data_ = {}
data_["item_id"] = data["data"]["id"]
data_[""] = data["data"]["title"]
data_["old_price"] = float(data["data"]["old_price"])
data_["current_price"] = float(data["data"]["price"])
data_["href"] = data["data"]["href"]
data_["brand"] = data["data"]["brand"]
data_["category"] = data["data"]["last_category"]["title"]

print(f"Filtered data: {data_=}")