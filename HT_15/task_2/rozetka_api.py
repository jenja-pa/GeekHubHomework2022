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
import requests
import json
from dataclasses import dataclass


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
    FILE_HEADERS = "headers.json"
    URL_API = "https://rozetka.com.ua/api/product-api/v4/goods/get-main"
    PARAMS = {"country": "UA", "lang": "ua", "goodsId": ""}

    def __init__(self):
        self._session = requests.Session()
        self.headers = self.FILE_HEADERS

    def _get_headers(self, file_name) -> dict:
        headers = {}
        with open(file_name, encoding="utf-8") as file:
            headers = json.load(file)
        return headers["header1"]

    @property
    def headers(self) -> dict:
        if self._headers is not None:
            return self._headers
        return {}

    @headers.setter
    def headers(self, f_name):
        self._headers = self._get_headers(f_name)

    def get_item_data(self, id: int) -> Data:
        params = dict(self.PARAMS)
        params["goodsId"] = id
        response = self._session.get(self.URL_API, headers=self.headers, params=params)
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
            print(f"Error getting id:{id} from rozetka DB")

        # todo - debug out data
        print(f"data_api: {result=}") 
        return result


if __name__ == "__main__":
    api = Api()
    result = api.get_item_data(27714809)
    print(f"rozetka_api.py: {result=}")