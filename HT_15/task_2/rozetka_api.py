# rozetka_api.py
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
# import json
from dataclasses import dataclass

import requests


@dataclass
class Data:
    item_id: int
    title: str 
    old_price: float 
    current_price: float 
    href: str 
    brand: str 
    category: str 


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
                )
        else:
            print(f"Error getting id:{item_id} from list of goods in the "
                  f"store rozetka DB")

        return result
