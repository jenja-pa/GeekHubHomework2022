"""
- rozetka_api.py, де створти клас RozetkaAPI, який буде містити
метод get_item_data, який на вхід отримує id товара з сайту розетки
та повертає словник з такими даними:
  * item_id (він же і приймається на вхід),
  * title,
  * old_price,
  * current_price,
  * href (лінка на цей товар на сайті),
  * brand,
  * category.
Всі інші методи, що потрібні для роботи мають бути приватні/захищені.
 * Якщо ID не валідний/немає даних - вивести відповідне повідомлення 
"""
from dataclasses import dataclass, asdict

import requests
from django.contrib import messages

from .models import Product
from .models import BackgroundProcessMessage


@dataclass
class Data:
    item_id: int
    title: str
    sell_status: str
    old_price: float
    current_price: float
    href: str
    brand: str
    category: str
    url_image_preview: str
    url_image_big: str


class Api:
    URL_API = "https://rozetka.com.ua/api/product-api/v4/goods/get-main"
    PARAMETERS = {"country": "UA", "lang": "ua", "goodsId": ""}

    def __init__(self, name_thread):
        self._session = requests.Session()
        self._name_thread = name_thread

    def get_item_data(self, item_id: str) -> Data:
        params = dict(self.PARAMETERS)
        params["goodsId"] = item_id
        response = self._session.get(
                 self.URL_API,
                 params=params)
        result = None
        if response.ok:
            data = response.json()["data"]
            result = Data(
                item_id=int(data["id"]),
                title=data["title"],
                sell_status=data["sell_status"],
                old_price=float(data["old_price"]),
                current_price=float(data["price"]),
                href=data["href"],
                brand=data["brand"],
                category=data["last_category"]["title"],
                url_image_preview=data["images"][0]["preview"]["url"],
                url_image_big=data["images"][0]["original"]["url"],
                )
        else:
            bg_mess = BackgroundProcessMessage(
                value=(f"{self._name_thread}: Помилка отримання інформації по "
                       f"id:{item_id} від і-магазина rozetka.com.ua")
            )
            bg_mess.save()

        return result


def get_data_from_scraper_and_put_into_db(lst_ids, name_thread):
    rozetka_api = Api(name_thread)
    count_success_requests = 0
    count_wrong_requests = 0
    count_insert_rows = 0
    count_update_rows = 0
    for item_id in lst_ids:
        if item_id:
            data = rozetka_api.get_item_data(item_id)
            if data:
                count_success_requests += 1

                # send data to DB
                _, created = Product.objects.update_or_create(
                    item_id=data.item_id,
                    defaults=asdict(data)
                    )
                if created:
                    count_insert_rows += 1
                else:
                    count_update_rows += 1
            else:
                count_wrong_requests += 1

    bg_mess = BackgroundProcessMessage(
        value=f"{name_thread}: Запитів (Успішних/Збійних): "
              f"({count_success_requests}/{count_wrong_requests}). "
              f"Всього: {count_success_requests + count_wrong_requests}."
        )
    bg_mess.save()
    bg_mess = BackgroundProcessMessage(
        value=f"{name_thread}: Операції з БД. (Вставлено/Поновлено): "
              f"({count_insert_rows}/{count_update_rows}). "
              f"Всього: {count_insert_rows + count_update_rows}."
        )
    bg_mess.save()
