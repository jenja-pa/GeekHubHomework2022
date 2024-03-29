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

from .models import Product
from .models import BackgroundProcessMessage


@dataclass
class Data:
    item_id: int
    title: str
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

    def __init__(self):
        self._session = requests.Session()

    def get_item_data(self, item_id: str) -> Data:
        params = dict(self.PARAMETERS)
        params["goodsId"] = item_id
        response = self._session.get(
                 self.URL_API,
                 params=params)
        result = None
        if response.ok:
            data = response.json()
            result = Data(
                item_id=int(data["data"]["id"]),
                title=data["data"]["title"],
                old_price=float(data["data"]["old_price"]),
                current_price=float(data["data"]["price"]),
                href=data["data"]["href"],
                brand=data["data"]["brand"],
                category=data["data"]["last_category"]["title"],
                url_image_preview=data["data"]["images"][0]["preview"]["url"],
                url_image_big=data["data"]["images"][0]["original"]["url"],
                )
        else:
            print(f"Error getting id:{item_id} from list of goods in the "
                  f"store rozetka DB")

        return result


def get_data_from_scraper_and_put_into_db(lst_ids):
    rozetka_api = Api()
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
        value=f"Запитів: "
              f"Успішних: {count_success_requests}, "
              f"Збійних: {count_wrong_requests}, "
              f"Всього: {count_success_requests + count_wrong_requests}."
              f" Операції з БД. "
              f"Вставлено {count_insert_rows}/"
              f"Поновлено {count_update_rows} рядків"
        )
    bg_mess.save()
