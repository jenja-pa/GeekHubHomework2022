# task_2.py
# Програма для отримання курсу валют за певний період.
#  - отримати від користувача дату (це може бути як один день так і інтервал
#     - початкова і кінцева дати, продумайте механізм реалізації) 
#  - назву валюти
#  - вивести курс по відношенню до гривні на момент вказаної дати (або за кожен 
# день у вказаному інтервалі)
#  - не забудьте перевірку на валідність введених даних

import json
from os.path import exists
from datetime import datetime as dt

from task_2_currency_exchange import CurrencyExchangeUAnbuScrapper
from task_2_rich_input import DatePromptCurrency


class CurrencyViewerApp:
    PATH_DATA_JSON = "task_2_currency.json"
    
    def __init__(self):
        # self._present_data = self.load_saved_data()
        self._present_data = {}
        self._get_remote_data = CurrencyExchangeUAnbuScrapper()
        now_str_date = dt.now().strftime('%d.%m.%Y')
        if now_str_date not in self._present_data.keys():
            currency_for_date = self._get_remote_data.get_site_currency_exchange_list(now_str_date)
            self._present_data[now_str_date] = currency_for_date

    # def load_saved_data(self):
    #     if exists(self.PATH_DATA_JSON):
    #         with open(self.PATH_DATA_JSON, encoding="utf-8") as f:
    #             return json.load(f)
    #     else:
    #         return {}
 
    # def save_present_data(self):
    #     with open(self.PATH_DATA_JSON, "w", encoding="utf-8") as f:
    #         json.dump(self._present_data, f)

    def get_data_for_date(self, str_date):
        # data = self._pre
        pass

    def get_seq_code_currence(self):
        str_date = dt.now().strftime('%d.%m.%Y')
        lst_exchange_date = self._present_data[str_date]["data"]
        lst_currensies = [item.char_code for item in lst_exchange_date]
        # print(f"get_seq_code_currence: {cur_date=}")
        return lst_currensies


if __name__ == "__main__":
    app = CurrencyViewerApp()
    print("Отримуємо курси валют за деякий період.")
    print("Дані отримані від https://bank.gov.ua/ за період 02.09.1996 по поточну дату")
    print("Наявні коди валют для застосування:")
    print("/".join(app.get_seq_code_currence()))

    # app.save_present_data()